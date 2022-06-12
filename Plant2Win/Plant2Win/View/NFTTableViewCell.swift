//
//  NFTTableViewCell.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit
import QuartzCore

class NFTTableViewCell: UITableViewCell {

    private let margin = 20
    public var treeImageView = UIImageView()
    private var tree:NFTree?
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
        
        treeImageView = UIImageView(frame: CGRect(x: margin, y: margin, width: 358 - margin, height: 358 - margin))
        print(treeImageView.frame)
        
        treeImageView.layer.cornerRadius = 5
        self.layer.cornerRadius = 5
        treeImageView.layer.masksToBounds = true
        self.layer.masksToBounds = true
        
        treeImageView.contentMode = .scaleAspectFit
        
        self.addSubview(treeImageView)
        
    }
    
    public func setNFT(newTree:NFTree){
        self.tree = newTree
        
        //self.treeImageView.backgroundColor = .red
        
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
