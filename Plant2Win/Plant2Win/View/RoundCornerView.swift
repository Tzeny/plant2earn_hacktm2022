//
//  RoundCornerView.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 12.06.2022.
//

import UIKit
import QuartzCore

class RoundCornerView: UIView {

    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
    }
    */
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        
        layer.cornerRadius = 5
        layer.masksToBounds = true
    }
    
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        
        layer.cornerRadius = 5
        layer.masksToBounds = true
    }
}
