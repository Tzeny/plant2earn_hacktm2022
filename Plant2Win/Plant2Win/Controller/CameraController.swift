//
//  FaceDetectionController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import UIKit
import AVFoundation
import Vision
import CoreImage
import CoreGraphics

protocol CameraControllerDelegate {
    func didReceiveCameraVideoOutput(frame: CVPixelBuffer)
    func faceBoundingBoxesUpdate(faceBoundingBoxes : [CAShapeLayer])
    func verifyFace(faceFrame: [CVPixelBuffer])
    func debug(image: UIImage)
}

protocol CameraLivenessDelegate {
    func processLandmark(landmark: VNFaceLandmarkRegion2D, boundingBox: CGRect, completionHandler: @escaping (MoveDirection?, Bool) -> Void)
}

class CameraController: NSObject {
        
    fileprivate var captureSession: AVCaptureSession?
    fileprivate var rearCamera: AVCaptureDevice?
    fileprivate var frontCamera: AVCaptureDevice?

    fileprivate var currentCameraPosition: CameraPosition?
    fileprivate var frontCameraInput: AVCaptureDeviceInput?
    fileprivate var rearCameraInput: AVCaptureDeviceInput?
    
    fileprivate var photoOutput: AVCapturePhotoOutput?
    fileprivate var previewLayer: AVCaptureVideoPreviewLayer?
    
    fileprivate let videoDataOutput = AVCaptureVideoDataOutput()
    
    // TODO: Refactor below since we now have multiple delegates
    public var delegate: CameraControllerDelegate?
    public var livenessDelegate: CameraLivenessDelegate?

}

extension CameraController: AVCaptureVideoDataOutputSampleBufferDelegate {
    
    func captureOutput(
        _ output: AVCaptureOutput,
        didOutput sampleBuffer: CMSampleBuffer,
        from connection: AVCaptureConnection) {
            
        guard let frame = CMSampleBufferGetImageBuffer(sampleBuffer) else {
            debugPrint("unable to get image from sample buffer")
            return
        }
        
        delegate?.didReceiveCameraVideoOutput(frame: frame)
    }
}

extension CameraController {
    
    public func handleFaceDetectionResults(_ observedFaces: [VNFaceObservation], frame: CVPixelBuffer) {
        
        guard let previewLayer = self.previewLayer else {
            fatalError("No Preview Layer")
        }
        
        let facesBoundingBoxesRects: [CGRect] = observedFaces.compactMap({ (observedFace: VNFaceObservation) -> CGRect in
            return previewLayer.layerRectConverted(fromMetadataOutputRect: observedFace.boundingBox)
            })
       
        
        let facesBoundingBoxes: [CAShapeLayer] = observedFaces.flatMap({ (observedFace: VNFaceObservation) -> [CAShapeLayer] in
            let faceBoundingBoxOnScreen = previewLayer.layerRectConverted(fromMetadataOutputRect: observedFace.boundingBox)
            let faceBoundingBoxPath = CGPath(rect: faceBoundingBoxOnScreen, transform: nil)
            
            let faceBoundingBoxShape = CAShapeLayer()
            faceBoundingBoxShape.path = faceBoundingBoxPath
            faceBoundingBoxShape.fillColor = UIColor.clear.cgColor
            faceBoundingBoxShape.strokeColor = UIColor.green.cgColor
            
            var newDrawings = [CAShapeLayer]()
            newDrawings.append(faceBoundingBoxShape)
            if let landmarks = observedFace.landmarks {
                newDrawings = newDrawings + self.drawFaceFeatures(landmarks, screenBoundingBox: faceBoundingBoxOnScreen)
            }
            return newDrawings
            
        })
        
        for faceBBox in facesBoundingBoxesRects {
            var allBBoxes = [CVPixelBuffer]()
        
            //This must be the size of the view that the video is previewed in instead of the UIScreen size - this works for now because the preview layer is fullscreen
            let screenWidth = UIScreen.main.bounds.size.width
            let screenHeight = UIScreen.main.bounds.size.height
            
            //Transform from one axis to another
            let ratioX = faceBBox.origin.x / screenWidth
            let ratioY = faceBBox.origin.y / screenHeight
            let ratioWidth = faceBBox.width / screenWidth
            let ratioHeight = faceBBox.height / screenHeight
            
            let bufX = ratioX * CGFloat(CVPixelBufferGetWidth(frame))
            let bufY = ratioY * CGFloat(CVPixelBufferGetHeight(frame))
            let bufWidth = ratioWidth * CGFloat(CVPixelBufferGetWidth(frame))
            let bufHeight = ratioHeight * CGFloat(CVPixelBufferGetHeight(frame))

            if let buf = frame.resizePixelBuffer(cropX: CVPixelBufferGetWidth(frame) - Int(bufX) - Int(bufWidth), cropY: Int(bufY), cropWidth: Int(bufWidth), cropHeight: Int(bufHeight), scaleWidth:  Int(bufWidth), scaleHeight: Int(bufHeight)) {
                
                allBBoxes.append(buf)
                
                //let ciImage = CIImage(cvPixelBuffer: buf)
                //let temporaryContext = CIContext(options: nil)
                
                //if let videoImage = temporaryContext.createCGImage(ciImage, from: CGRect(x: 0, y: 0, width:CVPixelBufferGetWidth(buf), height:CVPixelBufferGetHeight(buf))){
                    //let image = UIImage(cgImage: videoImage)
                    
                //}
                
            }
            
            delegate?.verifyFace(faceFrame: allBBoxes)
        }
        
        delegate?.faceBoundingBoxesUpdate(faceBoundingBoxes: facesBoundingBoxes)
    }
    
    private func drawFaceFeatures(_ landmarks: VNFaceLandmarks2D, screenBoundingBox: CGRect) -> [CAShapeLayer] {
        var faceFeaturesDrawings: [CAShapeLayer] = []
        
        if let leftEye = landmarks.leftEye {
            let eyeDrawing = self.drawPoints(leftEye, screenBoundingBox: screenBoundingBox)
            faceFeaturesDrawings.append(eyeDrawing)
        }
        
        if let rightEye = landmarks.rightEye {
            let eyeDrawing = self.drawPoints(rightEye, screenBoundingBox: screenBoundingBox)
            faceFeaturesDrawings.append(eyeDrawing)
        }
        
        if let leftPupil = landmarks.leftPupil {
            livenessDelegate?.processLandmark(landmark: landmarks.leftPupil!, boundingBox: screenBoundingBox, completionHandler: {_,_ in })
        }
        if let rightPupil = landmarks.rightPupil {
            let drawing = self.drawPoints(rightPupil, screenBoundingBox: screenBoundingBox)
            faceFeaturesDrawings.append(drawing)
        }
        if let medianLine = landmarks.medianLine {
            let drawing = self.drawPoints(medianLine, screenBoundingBox: screenBoundingBox)
            faceFeaturesDrawings.append(drawing)
        }
        if let medianLine = landmarks.outerLips {
            let drawing = self.drawPoints(medianLine, screenBoundingBox: screenBoundingBox)
            faceFeaturesDrawings.append(drawing)
        }
        if let medianLine = landmarks.noseCrest {
            let drawing = self.drawPoints(medianLine, screenBoundingBox: screenBoundingBox)
            faceFeaturesDrawings.append(drawing)
            }
        // draw other face features here
        return faceFeaturesDrawings
    }
    
    private func drawPoints(_ region: VNFaceLandmarkRegion2D, screenBoundingBox: CGRect) -> CAShapeLayer {
        let path = CGMutablePath()
        let pathPoints = region.normalizedPoints
            .map({ point in
                CGPoint(
                    x: point.y * screenBoundingBox.height + screenBoundingBox.origin.x,
                    y: point.x * screenBoundingBox.width + screenBoundingBox.origin.y)
             })
        path.addLines(between: pathPoints)
        path.closeSubpath()
        let drawing = CAShapeLayer()
        drawing.path = path
        drawing.fillColor = UIColor.clear.cgColor
        drawing.strokeColor = UIColor.green.cgColor
        
        return drawing
    }
}

extension CameraController {
    
    public func prepare(completionHandler: @escaping (Error?) -> Void) {
            
            func createCaptureSession() {
                self.captureSession = AVCaptureSession()
            }
            
            func configureCaptureDevices() throws {
                
                let session = AVCaptureDevice.DiscoverySession(deviceTypes: [.builtInWideAngleCamera], mediaType: AVMediaType.video, position: .unspecified)
                
                var cameras = [AVCaptureDevice]()
                
                for camera in session.devices {
                    cameras.append(camera)
                }
               
                if cameras.isEmpty {
                    throw CameraControllerError.noCamerasAvailable
                }

                 
                for camera in cameras {
                    if camera.position == .front {
                        self.frontCamera = camera
                    }
                    
    //                if camera.position == .back {
    //                    self.rearCamera = camera
    //
    //                    try camera.lockForConfiguration()
    //                    camera.focusMode = .continuousAutoFocus
    //                    camera.unlockForConfiguration()
    //                }
                }
            }
            
            func configureDeviceInputs() throws {
                
                guard let captureSession = self.captureSession else { throw CameraControllerError.captureSessionIsMissing }
                
                   
    //               if let rearCamera = self.rearCamera {
    //                   self.rearCameraInput = try AVCaptureDeviceInput(device: rearCamera)
    //
    //                   if captureSession.canAddInput(self.rearCameraInput!) { captureSession.addInput(self.rearCameraInput!) }
    //
    //                   self.currentCameraPosition = .rear
    //               }else
                
                if let frontCamera = self.frontCamera {
                
                    self.frontCameraInput = try AVCaptureDeviceInput(device: frontCamera)
                
                    if captureSession.canAddInput(self.frontCameraInput!) { captureSession.addInput(self.frontCameraInput!) }
                    else { throw CameraControllerError.inputsAreInvalid }
            
                    self.currentCameraPosition = .front
                }
                else { throw CameraControllerError.noCamerasAvailable }
                
            }
            
            func configureCameraOutput() throws {
                guard let captureSession = self.captureSession else { throw CameraControllerError.captureSessionIsMissing }
                
                self.videoDataOutput.videoSettings = [(kCVPixelBufferPixelFormatTypeKey as NSString) : NSNumber(value: kCVPixelFormatType_32BGRA)] as [String : Any]
                self.videoDataOutput.alwaysDiscardsLateVideoFrames = true
                self.videoDataOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "camera_frame_processing_queue"))
                
                if captureSession.canAddOutput(videoDataOutput) { captureSession.addOutput(videoDataOutput) }
                
                guard let connection = self.videoDataOutput.connection(with: AVMediaType.video),
                    connection.isVideoOrientationSupported else { return }
                
                connection.videoOrientation = .portrait
                captureSession.startRunning()
            }
            
            DispatchQueue(label: "prepare").async {
                do {
                    createCaptureSession()
                    try configureCaptureDevices()
                    try configureDeviceInputs()
                    try configureCameraOutput()
                }
                    
                catch {
                    DispatchQueue.main.async {
                        completionHandler(error)
                    }
                    
                    return
                }
                
                DispatchQueue.main.async {
                    completionHandler(nil)
                }
            }
        }
    


    public func displayPreview(on view: UIView) throws {
        guard let captureSession = self.captureSession, captureSession.isRunning else { throw CameraControllerError.captureSessionIsMissing }

        self.previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        self.previewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
        self.previewLayer?.connection?.videoOrientation = .portrait

        view.layer.insertSublayer(self.previewLayer!, at: 0)
        self.previewLayer?.frame = view.frame
    }
    
    public func close(){
        guard let captureSession = self.captureSession, captureSession.isRunning else { return }
        
        captureSession.stopRunning()
    }
}

extension CameraController {
    public enum CameraPosition {
        case front
        case rear
    }
    
    enum CameraControllerError: Swift.Error {
            case captureSessionAlreadyRunning
            case captureSessionIsMissing
            case inputsAreInvalid
            case invalidOperation
            case noCamerasAvailable
            case noOutput
            case unknown
    }
}
