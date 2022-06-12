//
//  LoaderView.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class LoaderView: UIView {

    @IBOutlet weak var textLabel: UILabel!
    @IBOutlet weak var spinnerImageView: SpinningImageView!
    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
    }
    */
    
    class func instanceFromNib() -> UIView {
        return UINib(nibName: "LoaderView", bundle: Bundle.main).instantiate(withOwner: nil, options: nil)[0] as! UIView
    }
    
    public func startSpinning(){
        
        self.spinnerImageView.rotate()
        
    }
    
    public func changeText(newText: String){
        
        UIView.transition(with: self.textLabel, duration: 0.25, options: .transitionCrossDissolve, animations: { [weak self] in
            
            self?.textLabel.text = newText
            
        }, completion: nil)
        
    }
    
    public func stopSpinning(){
        self.spinnerImageView.stop()
    }

}


