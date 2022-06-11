//
//  TreeTypeViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class TreeTypeViewController: UIViewController {

    @IBOutlet weak var takePhotoButton: UIButton!
    private let cameraController = CameraController()
    private var captureImage = false
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        cameraController.prepare(camPosition: .back, completionHandler: {(error) in
            if let error = error {
                print(error)
            }
            
            let previewView = UIView(frame: self.view.frame)
            self.view.addSubview(previewView)
            self.view.sendSubviewToBack(previewView)
            
            //Begin processing images from the camera
            try? self.cameraController.displayPreview(on: previewView)
        })

        cameraController.delegate = self
    }
    

    @IBAction func takePhoto(_ sender: UIButton) {
        
        captureImage = true
        
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


extension TreeTypeViewController: CameraControllerDelegate {
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
        
        DispatchQueue.main.async {
            if self.captureImage {
                
                let ci = CIImage(cvPixelBuffer: frame)
                let tempContext = CIContext(options: nil)
                
                guard let videoImage = tempContext.createCGImage(ci, from: CGRect(x: 0, y: 0, width: CVPixelBufferGetWidth(frame), height: CVPixelBufferGetHeight(frame))) else {return}
                
                let image = UIImage(cgImage: videoImage)
                
                print("got image")
                
                let previewImage = UIImageView(frame: UIScreen.main.bounds)
                self.view.addSubview(previewImage)
                
                previewImage.image = image
                previewImage.contentMode = .scaleAspectFit
                
                self.cameraController.close()
                self.cameraController.delegate = nil
                
                self.view.bringSubviewToFront(self.takePhotoButton)
            }
        }
        

    }
    
    func didCaptureImage(image: UIImage) {
        
    
        
    }
    
}
