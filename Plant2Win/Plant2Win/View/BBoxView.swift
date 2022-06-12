//
//  BBoxView.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit

class BBoxView: ClockworkView {

    private var topView:UIView
    private let bottomView:UIView
    private let rightView:UIView
    private let leftView:UIView

    private static let width = 5
    
    public init(frame: CGRect, color:UIColor) {
        
        topView = UIView(frame: CGRect(x: 0, y: 0, width: Int(frame.width), height: BBoxView.width))
        bottomView = UIView(frame: CGRect(x: 0, y: Int(frame.height) - BBoxView.width, width: Int(frame.width), height: BBoxView.width))
        
        rightView = UIView(frame: CGRect(x: Int(frame.width) - BBoxView.width, y: 0, width: BBoxView.width, height: Int(frame.height)))
        leftView = UIView(frame: CGRect(x: 0, y: 0, width: BBoxView.width, height: Int(frame.height)))
        
        leftView.backgroundColor = color
        topView.backgroundColor = color
        bottomView.backgroundColor = color
        rightView.backgroundColor = color
        
        super.init(frame: frame)
        
        self.addSubview(leftView)
        self.addSubview(topView)
        self.addSubview(bottomView)
        self.addSubview(rightView)
        
        backgroundColor = UIColor(white: 1, alpha: 0)
        
        isHidden = true
    }
    
    required init?(coder aDecoder: NSCoder) {
        
        topView = UIView()
        bottomView = UIView()
        
        rightView = UIView()
        leftView = UIView()
        
        super.init(coder: aDecoder)
    }
    

}
