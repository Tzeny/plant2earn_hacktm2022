//
//  LoaderController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class LoaderController: NSObject {

    let view = LoaderView.instanceFromNib() as! LoaderView
    private var currentTextIndex = 0
    private var textArray:[String] = []
    private var timer = Timer()
    
    public func presentView(withTextArray text:[String]){
        
        UIView.animate(withDuration: 1, delay: 0, options: UIView.AnimationOptions.transitionCrossDissolve, animations: {
            self.view.isHidden = false
        }, completion: {_ in
            self.view.startSpinning()
            
            self.textArray = text
            
            self.changeText()
            
        })
        

        
    
    }
    
    private func changeText(){
        
        self.timer.invalidate()
        print(self.textArray[self.currentTextIndex])
        
        DispatchQueue.main.async {
            self.view.changeText(newText: self.textArray[self.currentTextIndex])
        }
        
        if currentTextIndex + 1 < textArray.count {
           
            self.timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: false, block: { _ in
                self.currentTextIndex = self.currentTextIndex + 1
                self.changeText()
            })
            
        }
        
    }
    
    public func stop(completion: @escaping() -> Void){
        UIView.animate(withDuration: 0.5, delay: 0, options: UIView.AnimationOptions.transitionCrossDissolve, animations: {
            self.view.isHidden = true
        }, completion: {_ in
            self.view.stopSpinning()
            completion()
        })
        
    }
    
}
