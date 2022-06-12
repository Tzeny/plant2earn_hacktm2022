//
//  TreeTypeViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class TreeTypeViewController: UIViewController {

    @IBOutlet weak var topView: UIView!
    @IBOutlet weak var takePhotoButton: UIButton!
    private let cameraController = CameraController()
    private var captureImage = false
    private let segmented = ClockworkView(frame: UIScreen.main.bounds)
    private var newNFTree:NFTree? = nil
    private var timer = Timer()
    
    private var loaderController = LoaderController()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        LocationController.shared.delegate = self
        
        navigationController?.navigationBar.backgroundColor = .white
        self.navigationItem.title = "STEP 3"
        let textAttributes = [NSAttributedString.Key.foregroundColor:UIColor.black]
        navigationController?.navigationBar.titleTextAttributes = textAttributes
        
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
    
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        
        LocationController.shared.delegate = nil
    }
    

    @IBAction func takePhoto(_ sender: UIButton) {
        
        captureImage = true
        
    }
    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
        
        if let dvc = segue.destination as? NFTreeViewController {
            dvc.tree = newNFTree
        }
        
    }
    

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
                if self.cameraController.delegate != nil {
                    let ci = CIImage(cvPixelBuffer: frame)
                    let tempContext = CIContext(options: nil)
                    
                    guard let videoImage = tempContext.createCGImage(ci, from: CGRect(x: 0, y: 0, width: CVPixelBufferGetWidth(frame), height: CVPixelBufferGetHeight(frame))) else {return}
                    
                    let image = UIImage(cgImage: videoImage)
                    
                    print("got image")
                    
                    let previewImage = UIImageView(frame: UIScreen.main.bounds)
                    self.view.addSubview(previewImage)
                    
                    previewImage.image = image
                    previewImage.contentMode = .scaleAspectFill
                    
                    self.cameraController.close()
                    self.cameraController.delegate = nil
                    
                    self.view.bringSubviewToFront(self.takePhotoButton)
                    
                    self.loaderController.presentView(withTextArray: ["text a", "text b", "text c..."])
                    self.view.addSubview(self.loaderController.view)
                    self.view.bringSubviewToFront(self.topView)
                    
                    if LocationController.shared.long == "0"{
                        LocationController.shared.getLocation()
                    }else{
                        
                        BackendController.shared.segmentLeaf(image: image, long: LocationController.shared.long, lat: LocationController.shared.lat, completion: {
                            firstImage, nft in
                            
                            self.newNFTree = nft
                            
                            self.segmented.isHidden = true
                            self.segmented.backgroundColor = .blue
                            
                            let imageView = UIImageView(frame: self.segmented.bounds)
                            imageView.image = firstImage
                            imageView.contentMode = .scaleAspectFill
                           
                            self.segmented.addSubview(imageView)
                            
                            self.view.addSubview(self.segmented)
                            self.view.bringSubviewToFront(self.topView)
                            self.loaderController.stop(completion: {
                                DispatchQueue.main.async {
                                    
                                    
                                    self.segmented.unHide()
                                    
                                    self.timer = Timer.scheduledTimer(withTimeInterval: 2, repeats: false, block: { _ in
                                        
                                        DispatchQueue.main.async {
                                            self.performSegue(withIdentifier: "NFTreeSegue", sender: nil)
                                        }
                                        
                                    })
                                    
                                    //
                                    print("Done")
                                }
                            })
                            
                            
                        })
                    }
                }
            }
        }
        

    }
    
    func didCaptureImage(image: UIImage) {
        
        
        
    }
    
}

extension TreeTypeViewController: LocationControllerDelegate {
    
    func gotCoords(lat:String, long:String){
        print(lat)
        print(long)
    }
}
