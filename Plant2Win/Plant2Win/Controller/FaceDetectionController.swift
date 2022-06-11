//
//  FaceDetectionController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import UIKit
import Vision

class FaceDetectionController: NSObject {

    public func detectFace(in image: CVPixelBuffer,  completionHandler: @escaping ([VNFaceObservation]? ) -> Void ) {
        
            let faceDetectionRequest = VNDetectFaceLandmarksRequest(completionHandler: { (request: VNRequest, error: Error?) in
            DispatchQueue.main.async {
                if let results = request.results as? [VNFaceObservation] {
                    completionHandler(results)
                } else {
                    completionHandler(nil)
                }
            }
        })
        let imageRequestHandler = VNImageRequestHandler(cvPixelBuffer: image, orientation: .leftMirrored, options: [:])
        try? imageRequestHandler.perform([faceDetectionRequest])
    }
    
    
    public func detectFace(in image: CGImage,  completionHandler: @escaping ([VNFaceObservation]? ) -> Void ) {
        
            let faceDetectionRequest = VNDetectFaceLandmarksRequest(completionHandler: { (request: VNRequest, error: Error?) in
            DispatchQueue.main.async {
                if let results = request.results as? [VNFaceObservation] {
                    completionHandler(results)
                } else {
                    completionHandler(nil)
                }
            }
        })
        
        let imageRequestHandler = VNImageRequestHandler(cgImage: image, orientation: .up, options: [:])
        try? imageRequestHandler.perform([faceDetectionRequest])
    }
    
}
