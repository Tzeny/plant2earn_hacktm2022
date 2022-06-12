const HDWalletProvider = require("@truffle/hdwallet-provider");

module.exports = {

  //configuring the networks
  networks: {
    development: {
      host: "127.0.0.1",  
      port: 7545,          
      network_id: "5777"
    },
    ropsten: {
      // must be a thunk, otherwise truffle commands may hang in CI
      provider: () =>
        new HDWalletProvider({
          privateKeys: ["872f3dee80ae96e40856c01bdd91cf332e7845aa669e001d335262dd04714a80"],
          providerOrUrl: "https://ropsten.infura.io/v3/c7d4a7dd4c414d8184e2e7acfe3a9057",
          numberOfAddresses: 1,
          shareNonce: true,
          derivationPath: "m/44'/1'/0'/0/"
        }),
      network_id: '3',
    }
  },


  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.13",
    }
  },
};
