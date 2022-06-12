//
//  NFTreeViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 11.06.2022.
//

import UIKit
import QuartzCore

class NFTreeViewController: UIViewController {

    @IBOutlet weak var NFTreeImageView: UIImageView!
    @IBOutlet weak var locationLabel: UILabel!
    @IBOutlet weak var valueLabel: UILabel!
    @IBOutlet weak var absorbtionLabel: UILabel!
    @IBOutlet weak var typeLabel: UILabel!
    
    public var tree:NFTree?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        NFTreeImageView.layer.cornerRadius = 5
        NFTreeImageView.layer.masksToBounds = true
        
        self.navigationItem.title = "OVERVIEW"
        let textAttributes = [NSAttributedString.Key.foregroundColor:UIColor.black]
        navigationController?.navigationBar.titleTextAttributes = textAttributes
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        if let url = tree?.imageURL, let abs = tree?.absorbtion, let prc = tree?.price, let ttype = tree?.treeType {
            NFTreeImageView.downloaded(from: url)
            self.absorbtionLabel.text = abs
            self.valueLabel.text = String(prc) + " ETH"
            self.navigationItem.title = ttype.uppercased()
        }
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        
        navigationController?.popToRootViewController(animated: true)
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
