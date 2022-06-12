//
//  SpinningImageView.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class SpinningImageView: UIImageView {

    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
    }
    */
    
    public func rotate(){
        
        self.image = UIImage(named: "spinner")
        self.backgroundColor = .clear
        let rotation : CABasicAnimation = CABasicAnimation(keyPath: "transform.rotation.z")
        rotation.toValue = NSNumber(value: Double.pi * 2)
        rotation.duration = 1
        rotation.isCumulative = true
        rotation.repeatCount = Float.greatestFiniteMagnitude
        self.layer.add(rotation, forKey: "rotationAnimation")
        
    }
    
    public func stop(){
        self.layer.removeAllAnimations()
    }

}
