//
//  LocationController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit
import CoreLocation

protocol LocationControllerDelegate {
    func gotCoords(lat:String, long:String)
}

class LocationController: NSObject {

    static let shared = LocationController()

    let locationManager = CLLocationManager()
    public var delegate:LocationControllerDelegate?
    public var long:String = "0"
    public var lat:String = "0"
    
    override private init(){
        
        super.init()
        
        locationManager.requestWhenInUseAuthorization()
        locationManager.delegate = self
    }
    
    public func getLocation(){
        locationManager.requestLocation()
    }
    
}

extension LocationController: CLLocationManagerDelegate {
    
    func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        if let location = locations.first {
            let latitude = location.coordinate.latitude
            let longitude = location.coordinate.longitude
            // Handle location update
            self.long = String(latitude)
            self.long = String(longitude)
            
            self.delegate?.gotCoords(lat: String(latitude), long: String(longitude))
            
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print(error)
    }
    
}
