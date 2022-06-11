//
//  LivenessGuard.swift
//  TrustBridge
//
//  Created by Daniel Giuriciu on 21/05/2020.
//  Copyright © 2020 Edgefront. All rights reserved.
//

import Foundation

//Models a simple liveness check module
class LivenessGuard: NSObject {
    
    public var leftMovementChecked = false;
    public var rightMovementChecked = false;
    public var upMovementChecked = false;
    public var downMovementChecked = false;
    
}
