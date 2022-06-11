//
//  FaceDetectionController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import Foundation
import Vision
import CoreGraphics

enum MoveDirection {
    case up
    case down
    case left
    case right
}

class LivenessController: NSObject {
    
    private var originalEyePos = CGPoint(x: 0, y:0)
    private let MOVEMENT_THRESHOLD = CGFloat(50)
    public var livenessGuard = LivenessGuard();
    private var tests = [MoveDirection]()
    
    //MARK: Init
    override public init(){
        
        //self.tests = [MoveDirection.left, MoveDirection.up,MoveDirection.right, MoveDirection.down]
        
        super.init()
    }
    
    func wasInitialized() -> Bool {
        return originalEyePos.x != 0 && originalEyePos.y != 0;
    }
    
    
    //MARK: Begin testing
    //Controller needs to know when to start verifying position. Can't do so right away, not natural for the user
    public func startTesting() {
        livenessGuard = LivenessGuard();
        
        self.tests = [MoveDirection.left, MoveDirection.up,MoveDirection.right, MoveDirection.down].shuffled()
    }
    
    //MARK: Position Calculation
    func updatePosition(newPosition: CGPoint) {
        self.originalEyePos = newPosition
    }
    
    func distanceX(_ point: CGPoint) -> CGFloat {
        return point.x - originalEyePos.x
    }
    
    func distanceY(_ point: CGPoint) -> CGFloat {
        return point.y - originalEyePos.y
    }
    
    //MARK: Position Checks
    func hasMovedUp(newPoint point: CGPoint) -> Bool {
        if (livenessGuard.upMovementChecked) {return true}
        
        if distanceY(point) < (-MOVEMENT_THRESHOLD){
            livenessGuard.upMovementChecked = true
            self.updatePosition(newPosition: point)
            return true
        }
        
        return false
    }
    
    func hasMovedDown(newPoint point: CGPoint) -> Bool {
        if (livenessGuard.downMovementChecked) {return true}
        
        if distanceY(point) > (MOVEMENT_THRESHOLD){
            livenessGuard.downMovementChecked = true
            self.updatePosition(newPosition: point)
            return true
        }
        
        return false
    }
    
    func hasMovedLeft(newPoint point: CGPoint) -> Bool {
        if (livenessGuard.leftMovementChecked) {return true}
        
        if distanceX(point) < (-MOVEMENT_THRESHOLD){
            livenessGuard.leftMovementChecked = true
            self.updatePosition(newPosition: point)
            return true
        }
        
        return false
    }
    
    func hasMovedRight(newPoint point: CGPoint) -> Bool {
        if (livenessGuard.rightMovementChecked) {return true}
        
        if distanceX(point) > (MOVEMENT_THRESHOLD){
            livenessGuard.rightMovementChecked = true
            self.updatePosition(newPosition: point)
            return true
        }
        
        return false
    }
    

    
}

//MARK: Update loop
extension LivenessController: CameraLivenessDelegate {
        
    // Can be generalized but for now just use this for the left pupil;
    
    //The completion block should update interface based on what happens with the tests. It returns the current test and a boolean indicating if it was passed since the last check or not

    func processLandmark(landmark: VNFaceLandmarkRegion2D, boundingBox: CGRect, completionHandler: @escaping (MoveDirection?, Bool) -> Void) {
        
        //The current test is the first in the array
        let currentTest = tests.first
        
        let pathPoint = landmark.normalizedPoints
        .map({ point in
            CGPoint(
                x: point.y * boundingBox.height + boundingBox.origin.x,
                y: point.x * boundingBox.width + boundingBox.origin.y)
            }).first
        
        print("LEFT PUPIL: \(pathPoint!)")
        print("LEFT: \(self.livenessGuard.leftMovementChecked) UP: \(self.livenessGuard.upMovementChecked) RIGHT: \(self.livenessGuard.rightMovementChecked) DOWN: \(self.livenessGuard.downMovementChecked)")
        
        if !wasInitialized() {
            updatePosition(newPosition: pathPoint!)
            print("initialized")
            
            return
        }
        
        
        //Check if challenge has been solved from last update
        if currentTest == .left {
            if hasMovedLeft(newPoint: pathPoint!){
                print("moved Left")
                tests.removeFirst()
                
                completionHandler(tests.first, true)
                return
            }
        }else if currentTest == .right {
            if hasMovedRight(newPoint: pathPoint!) {
                print("moved Right")
                tests.removeFirst()
                
                completionHandler(tests.first, true)
                return
            }
        }else if currentTest == .up {
            if hasMovedUp(newPoint: pathPoint!) {
                print("moved up")
                tests.removeFirst()
                
                completionHandler(tests.first, true)
                return
            }
        }else if currentTest == .down {
            if hasMovedDown(newPoint: pathPoint!) {
                print("moved down")
                tests.removeFirst()
                
                completionHandler(tests.first, true)
                return
            }
        }else{
            //Update position regardless of challenge being solved
            print("updating position")
            updatePosition(newPosition: pathPoint!)
        }
        
        completionHandler(currentTest, false)
    }
    
}


