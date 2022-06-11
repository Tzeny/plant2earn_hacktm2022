//
//  FaceIDLogin.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import UIKit
import LocalAuthentication

class FaceIDLogin: NSObject {

    let context:LAContext
    let biometry:LABiometryType
    let permissions:Bool
    
    override init(){
        
        context = LAContext()
        biometry = context.biometryType
        
        var error: NSError?

        // Check for biometric authentication
        // permissions
        permissions = context.canEvaluatePolicy(
            .deviceOwnerAuthentication,
            error: &error
        )
    }
    
    
    public func auth(success: @escaping () -> Void, failure: @escaping () -> Void){
        
        if !permissions {
            print("permission was denied")
        }
        
        let reason = "Log in with Face ID"
        
        context.evaluatePolicy(
            // .deviceOwnerAuthentication allows
            // biometric or passcode authentication
            .deviceOwnerAuthentication,
            localizedReason: reason
        ) { worked, error in
            if worked {
                success()
            } else {
                failure()
            }
        }
    }
    
    
}
