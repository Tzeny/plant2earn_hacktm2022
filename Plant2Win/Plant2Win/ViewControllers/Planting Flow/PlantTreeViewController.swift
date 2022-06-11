//
//  PlantTreeViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import UIKit
import Foundation
import Vision
import AudioToolbox
import AVFoundation


class PlantTreeViewController: UIViewController {

    @IBOutlet weak var taskLabel: UILabel!
    private let cameraController = CameraController()
    private let livenessController = LivenessController()
    fileprivate let faceDetector = FaceDetectionController()
    
    private var drawings: [CAShapeLayer] = []
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.taskLabel.text = nil
        self.taskLabel.isHidden = true
        
        // Do any additional setup after loading the view.
        cameraController.prepare(camPosition: .front, completionHandler:
        
            { (error) in
                if let error = error {
                    print(error)
                }
                
                let previewView = UIView(frame: self.view.frame)
                self.view.addSubview(previewView)
                self.view.sendSubviewToBack(previewView)
                
                //Begin processing images from the camera
                try? self.cameraController.displayPreview(on: previewView)
            }
                                    
        )
        
        cameraController.delegate = self
        cameraController.livenessDelegate = self
    }
    
    fileprivate func clearDrawings() {
        self.drawings.forEach({ drawing in drawing.removeFromSuperlayer() })
    }
    
    fileprivate func description(from direction:MoveDirection) -> String {
        
        
        let descriptionString = "Please tilt your head "
        
        if direction == .up {
            return descriptionString + "up"
        }else if direction == .down {
            return descriptionString + "down"
        }else if direction == .left {
            return descriptionString + "left"
        }else{
            return descriptionString + "right"
        }
        
    }
    

    @IBAction func startButtonClicked(_ sender: UIButton) {
        
        sender.isHidden = true
        self.livenessController.startTesting()
    }
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}

extension PlantTreeViewController: CameraLivenessDelegate {
    
    func processLandmark(landmark: VNFaceLandmarkRegion2D, boundingBox: CGRect, completionHandler: @escaping (MoveDirection?, Bool) -> Void) {
        
        self.livenessController.processLandmark(landmark: landmark, boundingBox: boundingBox, completionHandler: { direction, success in
            
            DispatchQueue.main.async {
                //If no text is in the label, initiate it with the currernt direction
                if self.taskLabel.text == nil, let currentDirection = direction {
                    self.taskLabel.text = self.description(from: currentDirection)
                    self.taskLabel.isHidden = false
                    return
                }
                
                if success {
                    //Play a sound and vibrate on success
                    AudioServicesPlaySystemSound(kSystemSoundID_Vibrate)
                    AudioServicesPlayAlertSound(1057)
                    
                    //If there is any direction left, update the label, otherwise the challenge is completed
                    if let currentDirection = direction {
                        self.taskLabel.text = self.description(from: currentDirection)
                        return
                    }else{
                        self.taskLabel.text = "Challenge completed!"
                        
                        //Stop the processing
                        self.cameraController.delegate = nil
                        self.cameraController.livenessDelegate = nil
                        self.clearDrawings()
                        
                        print("passed")
                        
                        AudioServicesPlaySystemSound(kSystemSoundID_Vibrate)
                        AudioServicesPlayAlertSound(1057)
                        
                        self.performSegue(withIdentifier: "SelfieVerificationSegue", sender: nil)
                        
                        return
                    }
                    
                }
            }
        })
    }
    
}




//This protocol is responsible for drawing contours on the screen. It also forwards the liveness check
extension PlantTreeViewController: CameraControllerDelegate {
    func verifyFace(faceFrame: [CVPixelBuffer]) {
//        print("This shuld never be called")
    }
    
    func debug(image: UIImage) {
//        print("This shouldn't ever be called either")
    }
    
    func faceBoundingBoxesUpdate(faceBoundingBoxes: [CAShapeLayer]) {
        
        faceBoundingBoxes.forEach({ faceBoundingBox in self.view.layer.addSublayer(faceBoundingBox) })
        self.drawings = faceBoundingBoxes
    }
    
    func didReceiveCameraVideoOutput(frame: CVPixelBuffer) {
        
        
        
        faceDetector.detectFace(in: frame, completionHandler: { faces in
            self.clearDrawings()
            if faces != nil {
                self.cameraController.handleFaceDetectionResults(faces!, frame: frame)
            }
        })
    }
    
    func didCaptureImage(image: UIImage) {
        
        print("got image")
        
    }
    
}
