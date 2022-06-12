//
//  SelfieVerificationViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class SelfieVerificationViewController: UIViewController {

    @IBOutlet weak var topView: UIView!
    @IBOutlet weak var takePhotoButton: UIButton!
    private let cameraController = CameraController()
    private var captureImage = false
    
    private var treeView:BBoxView?
    private var humanView:BBoxView?
    
    private var loaderController = LoaderController()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        navigationController?.navigationBar.backgroundColor = .white
        self.navigationItem.title = "STEP 2"
        let textAttributes = [NSAttributedString.Key.foregroundColor:UIColor.black]
        navigationController?.navigationBar.titleTextAttributes = textAttributes
        
        cameraController.prepare(camPosition: .front, completionHandler: {(error) in
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
        
        if captureImage {
            
            self.performSegue(withIdentifier: "TreeTypeSegue", sender: nil)
            
        }
        
        self.captureImage = true
        
        
    }
    
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */
    
    private func frameFromPoints(x1:Double, y1:Double, x2:Double, y2:Double) -> CGRect {
        
        return CGRect(x: x1, y: y1, width: x2-x1, height: y2-y1)
        
    }

}


//This protocol is responsible for drawing contours on the screen. It also forwards the liveness check
extension SelfieVerificationViewController: CameraControllerDelegate {
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
                if self.cameraController.delegate != nil {
                    self.takePhotoButton.imageView?.image = UIImage()
                    let ci = CIImage(cvPixelBuffer: frame)
                    let tempContext = CIContext(options: nil)
                    
                    guard let videoImage = tempContext.createCGImage(ci, from: CGRect(x: 0, y: 0, width: CVPixelBufferGetWidth(frame), height: CVPixelBufferGetHeight(frame))) else {return}
                    
                    let image = UIImage(cgImage: videoImage)
                    
                    print("got image")
                    
                    let previewImage = UIImageView(frame: UIScreen.main.bounds)
                    self.view.addSubview(previewImage)
                    
                    previewImage.image = image.withHorizontallyFlippedOrientation()
                    previewImage.contentMode = .scaleAspectFill
                    
                    self.cameraController.close()
                    self.cameraController.delegate = nil
                    
                    self.view.bringSubviewToFront(self.takePhotoButton)
                
                    self.loaderController.presentView(withTextArray: ["text a", "text b", "text c..."])
                    self.view.addSubview(self.loaderController.view)
                    self.view.bringSubviewToFront(self.topView)
                    
                    BackendController.shared.detectTree(image: image.withHorizontallyFlippedOrientation(), completion: {
                        treeCords,humanCords in
                        
                        let treeFrame = self.frameFromPoints(x1: treeCords[0], y1: treeCords[1], x2: treeCords[2], y2: treeCords[3])
                        let humanFrame = self.frameFromPoints(x1: humanCords[0], y1: humanCords[1], x2: humanCords[2], y2: humanCords[3])
                        
                        self.treeView = BBoxView(frame: treeFrame, color: .green)
                        self.humanView = BBoxView(frame: humanFrame, color: .blue)
                        self.treeView?.isHidden = true
                        self.humanView?.isHidden = true
                        
                        self.loaderController.stop(completion: {
                            DispatchQueue.main.async {
                                
                                self.view.addSubview(self.treeView!)
                                self.view.addSubview(self.humanView!)
                                
                                self.treeView?.unHide()
                                self.humanView?.unHide()
                                
                                self.view.bringSubviewToFront(self.takePhotoButton)
                                //self.performSegue(withIdentifier: "TreeTypeSegue", sender: nil)
                                print("Done")
                            }
                        })
                    })
                }
            }
        }
        

    }
    
    func didCaptureImage(image: UIImage) {
        
        
        
    }
    
}
