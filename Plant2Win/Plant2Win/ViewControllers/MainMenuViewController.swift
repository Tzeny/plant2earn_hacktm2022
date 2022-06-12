//
//  MainMenuViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import UIKit
import QuartzCore

class MainMenuViewController: UIViewController {

    @IBOutlet weak var nrForest: UILabel!
    @IBOutlet weak var valueLabel: UILabel!
    @IBOutlet weak var absorbptionLabel: UILabel!
    @IBOutlet weak var valueView: RoundCornerView!
    @IBOutlet weak var plantButton: UIButton!
    @IBOutlet weak var value: UILabel!
    @IBOutlet weak var absorbtion: UILabel!
    @IBOutlet weak var tableView: UITableView!
    var faceID = FaceIDLogin()

    private var NFTrees: [NFTree] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        LocationController.shared.getLocation()
        
        let imageView = UIImageView(frame: CGRect(x: 0, y: 0, width: 117, height: 20))
        
        imageView.image = UIImage(named: "logo.png")
        
        self.valueView.layer.borderWidth = 1
        self.valueView.layer.borderColor = UIColor.gray.cgColor
        
        
        self.navigationItem.titleView =  imageView
        self.plantButton.layer.borderWidth = 2
        self.plantButton.layer.borderColor = UIColor.white.cgColor
        self.plantButton.layer.cornerRadius = 5
        
        BackendController.shared.getNFTs {nftrees in
            self.NFTrees = nftrees
            DispatchQueue.main.async {
                
                var abs:Double = 0
                var val:Double = 0
                
                for tree in nftrees {
                    abs += Double(tree.absorbtion.dropLast())!
                    val += tree.price
                }
                
                self.nrForest.text = String(nftrees.count)
                self.absorbptionLabel.text = String(format: "%.2f T", abs)
                self.valueLabel.text = String(format: "%.2f ETH", val)
                self.tableView.reloadData()
            }
        }

    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
       
        tableView.backgroundView?.backgroundColor = .white
        tableView.backgroundColor = .white
        
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
    
    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
        
        if let dvc = segue.destination as? NFTreeViewController, let tree = sender as? NFTree {
            dvc.tree = tree
        }
    }
    

}


extension MainMenuViewController : UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return NFTrees.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let tree = NFTrees[indexPath.item]
        
        let cell:NFTTableViewCell = self.tableView.dequeueReusableCell(withIdentifier: "NFTreeTableViewCell") as! NFTTableViewCell
                
        cell.backgroundColor = .white
        // set the text from the data model
        cell.setNFT(newTree: tree)

        cell.treeImageView.downloaded(from: NFTrees[indexPath.item].imageURL, contentMode: .scaleToFill)

            
          
    
        return cell
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 358
    }
    
}


extension MainMenuViewController : UITableViewDelegate {
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.performSegue(withIdentifier: "NFTreeSegue", sender: NFTrees[indexPath.item])
        
        self.tableView.deselectRow(at: indexPath, animated: true)
        
    }
    
    
    
    
}

extension UIImageView {
    func downloaded(from url: URL, contentMode mode: ContentMode = .scaleAspectFit) {
        contentMode = mode
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard
                let httpURLResponse = response as? HTTPURLResponse, httpURLResponse.statusCode == 200,
                let mimeType = response?.mimeType, mimeType.hasPrefix("image"),
                let data = data, error == nil,
                let image = UIImage(data: data)
                else { return }
            DispatchQueue.main.async() { [weak self] in
                self?.image = image
            }
        }.resume()
    }
    func downloaded(from link: String, contentMode mode: ContentMode = .scaleAspectFit) {
        guard let url = URL(string: link) else { return }
        downloaded(from: url, contentMode: mode)
    }
}
