//
//  NFTree.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class NFTree: NSObject {

    public let absorbtion:String
    public let imageURL:String
    public let treeType:String
    public let price:Double
    

    init(jsonDict: Dictionary<String, Any>){
        
        absorbtion = jsonDict["co2_absorbtion"] as! String
        imageURL = jsonDict["nft_url"] as! String
        treeType = jsonDict["tree_type"] as! String
        let prices = jsonDict["price"] as! Array<Dictionary<String, Any>>
        
        let priceString = prices.last!["price"]
        
        price = Double(priceString as! String)!
        
    }
    
}
