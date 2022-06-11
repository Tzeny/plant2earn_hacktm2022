//
//  SelfieVerificationViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class SelfieVerificationViewController: UIViewController {

    private let cameraController = CameraController()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        cameraController.prepare {(error) in
            if let error = error {
                print(error)
            }
            
            let previewView = UIView(frame: self.view.frame)
            self.view.addSubview(previewView)
            self.view.sendSubviewToBack(previewView)
            
            //Begin processing images from the camera
            try? self.cameraController.displayPreview(on: previewView)
        }
        cameraController.delegate = self
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



//This protocol is responsible for drawing contours on the screen. It also forwards the liveness check
extension PlantTreeViewController: CameraControllerDelegate {
    func verifyFace(faceFrame: [CVPixelBuffer]) {
//        print("This shuld never be called")
    }
    
    func debug(image: UIImage) {
//        print("This shouldn't ever be called either")
    }
    
    func faceBoundingBoxesUpdate(faceBoundingBoxes: [CAShapeLayer]) {
        
        //faceBoundingBoxes.forEach({ faceBoundingBox in self.view.layer.addSublayer(faceBoundingBox) })
        //self.drawings = faceBoundingBoxes
    }
    
    func didReceiveCameraVideoOutput(frame: CVPixelBuffer) {
        
        //faceDetector.detectFace(in: frame, completionHandler: { faces in
        //    self.clearDrawings()
        //    if faces != nil {
        //        self.cameraController.handleFaceDetectionResults(faces!, frame: frame)
        //    }
        //})
    }
    
}
