//
//  ClockworkView.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class ClockworkView: UIView {

    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
    }
    */
    
    public func unHide(){
        
        UIView.transition(with: self, duration: 2, options: .transitionCrossDissolve, animations: {
            self.isHidden = false
        }, completion: {_ in
            
        })
    }
}
