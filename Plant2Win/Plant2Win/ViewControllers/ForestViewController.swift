//
//  ForestViewController.swift
//  Plant2Win
//
//  Created by Stefan Iarca on 10.06.2022.
//

import UIKit

class ForestViewController: UIViewController {

    @IBOutlet weak var ethValue: UILabel!
    @IBOutlet weak var offsetLabel: UILabel!
    @IBOutlet weak var tableView: UITableView!
    private var NFTrees: [NFTree] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    

    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
        
        if let dvc = segue.destination as? NFTreeViewController {
            dvc.tree = sender as? NFTree
            
        }
        
    }
    

}

extension ForestViewController : UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return NFTrees.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let tree = NFTrees[indexPath.item]
        
        let cell:NFTTableViewCell = self.tableView.dequeueReusableCell(withIdentifier: "NFTreeTableViewCell") as! NFTTableViewCell
        
        // set the text from the data model
        cell.setNFT(newTree: tree)
    
        return cell
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        print(UIScreen.main.bounds.size.height / 3)
        return UIScreen.main.bounds.size.height / 3
    }
    
}


extension ForestViewController : UITableViewDelegate {
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.performSegue(withIdentifier: "NFTreeSegue", sender: NFTrees[indexPath.item])
        
    }
    
    
}
