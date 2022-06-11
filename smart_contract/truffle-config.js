
module.exports = {

  //configuring the networks
  networks: {
    development: {
      host: "127.0.0.1",  
      port: 7545,          
      network_id: "5777"
    },

  },


  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.13",
    }
  },
};
