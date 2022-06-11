//
//  MainMenuViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import UIKit

class MainMenuViewController: UIViewController {

    var faceID = FaceIDLogin()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        
        faceID.auth(success: {
            
            print("great success")
        
        }, failure: {
        
            print("big fail")
        
        })
    }
    
    @IBAction func plantSeguePressed(_ sender: UIButton) {
        
        self.performSegue(withIdentifier: "PlantTreeSegue", sender: sender)
    }
    
    @IBAction func myForestPressed(_ sender: UIButton) {
        self.performSegue(withIdentifier: "MyForestSegue", sender: sender)
    }
    
    @IBAction func signupPressed(_ sender: UIButton) {
        self.performSegue(withIdentifier: "SignUpSegue", sender: sender)
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
