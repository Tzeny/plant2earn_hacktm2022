//
//  BackendController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit
import Alamofire

class BackendController: NSObject {

    static let shared = BackendController()
    static let compressioon = 0.2
    private override init() {
        super.init()
    }
    
    public func detectTree(image:UIImage, completion: @escaping (_ tree: Array<Double>, _ human:Array<Double>) -> Void) {
        
        guard let imgData = image.withHorizontallyFlippedOrientation().jpegData(compressionQuality: BackendController.compressioon) else {return}
        
        let date = Date(timeIntervalSince1970: 1480134638.0)
        let strDate = DateFormatter().string(from: date)
        
        
        AF.upload(multipartFormData: { multipartData in
            
            multipartData.append(imgData, withName: "file" , fileName:strDate)
            
        }, to: "https://backend.plant2win.com/hacktm/detect_tree").uploadProgress(queue: .main, closure: { progress in
            
            print("Upload Progress: \(progress.fractionCompleted)")
            
        }).responseJSON(completionHandler: { AFData in
            
            print(AFData)
            //we've got the response here
            guard let data = AFData.data else {return}
            let asJSON = try? JSONSerialization.jsonObject(with: data)
           
            let jsonDict = asJSON as? Dictionary<String, Any>
            
            let treeCoords = jsonDict?["coord_copac"] as! Array<Double>
            let humanCoords = jsonDict?["coord_om"] as! Array<Double>
            
            let scaledHuCoords = [
                Double(UIScreen.main.bounds.size.width - humanCoords[2] * UIScreen.main.bounds.size.width / image.size.width),
                Double(humanCoords[1] * UIScreen.main.bounds.size.height / image.size.height),
                Double(UIScreen.main.bounds.size.width - humanCoords[0] * UIScreen.main.bounds.size.width / image.size.width),
                Double(humanCoords[3] * UIScreen.main.bounds.size.height / image.size.height)]
            
            let scaledTrCoords = [
                Double(UIScreen.main.bounds.size.width - treeCoords[2] * UIScreen.main.bounds.size.width / image.size.width),
                Double(treeCoords[1] * UIScreen.main.bounds.size.height / image.size.height),
                Double(UIScreen.main.bounds.size.width - treeCoords[0] * UIScreen.main.bounds.size.width / image.size.width),
                Double(treeCoords[3] * UIScreen.main.bounds.size.height / image.size.height)  ]
            
            print(humanCoords)
            print(scaledHuCoords)
            
            print(treeCoords)
            print(scaledTrCoords)
            
            completion(scaledTrCoords, scaledHuCoords)
        })
    }
    
    public func segmentLeaf(image:UIImage, long:String, lat:String, completion: @escaping (_ firstImage: UIImage, _ nft: NFTree) -> Void) {
        
        guard let imgData = image.jpegData(compressionQuality: BackendController.compressioon) else {return}
        let date = Date(timeIntervalSince1970: 1480134638.0)
        let strDate = DateFormatter().string(from: date)
        
        AF.upload(multipartFormData: { multipartData in
            
            multipartData.append(imgData, withName: "file", fileName:strDate)
            
            guard let longData = long.data(using: .utf8) else {return}
            guard let latData = lat.data(using: .utf8) else {return}
            multipartData.append(latData, withName: "lat", fileName:"lat")
            multipartData.append(longData, withName: "long", fileName:"long")
            
            
        }, to: "https://backend.plant2win.com/hacktm/segment_leaf").uploadProgress(queue: .main, closure: { progress in
            
            print("Upload Progress: \(progress.fractionCompleted)")
            
        }).responseJSON(completionHandler: { AFData in
            
            //we've got the response here
            print(AFData)
            //we've got the response here
            guard let data = AFData.data else {return}
            let asJSON = try? JSONSerialization.jsonObject(with: data)
           
            let jsonDict = asJSON as? Dictionary<String, Any>
            
            let stringURL = jsonDict?["bbox_path"] as! String
            
            let nftDict = jsonDict?["nft_entry"] as! Dictionary<String, Any>
            let nftree = NFTree(jsonDict: nftDict)
            
            print(nftree.imageURL)
            print(nftree.absorbtion)
            
            AF.request(stringURL, method: .get, parameters: nil, encoding: URLEncoding.default, headers: nil, interceptor: nil, requestModifier: nil).responseData(completionHandler: { imageData in
                
                guard let image = UIImage(data: imageData.data!) else {return}
                print(imageData)
                print(image)
                
                completion(image, nftree)
                
            })
            
            
            
        })
    }
    
    public func getNFTs( completion: @escaping (_ nftrees: Array<NFTree>) -> Void) {
                
    
        AF.request("https://backend.plant2win.com/hacktm/nft/retrieve", method: .get, parameters: nil, encoding: URLEncoding.default, headers: nil, interceptor: nil, requestModifier: nil).responseJSON(completionHandler: {
            AFData in
            
            print(AFData)
            //we've got the response here
            guard let data = AFData.data else {return}
            let asJSON = try? JSONSerialization.jsonObject(with: data)
            let dicts = asJSON as! Array<Dictionary<String, Any>>
            
            var nftrees:Array<NFTree> = []
            
            for item in dicts {
                nftrees.append( NFTree(jsonDict: item) )
            }
            
            completion(nftrees)
            
        })
    }
    
    public func getImage(url:String, completion: @escaping (_ image: UIImage) -> Void) {
                
    
        AF.request(url, method: .get, parameters: nil, encoding: URLEncoding.default, headers: nil, interceptor: nil, requestModifier: nil).responseData(completionHandler: { imageData in
            
            guard let image = UIImage(data: imageData.data!) else {return}
            print(imageData)
            print(image)
            
            completion(image)
            
        })
        
    }
}
