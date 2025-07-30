# Load contract ABI and address
usdc_abi = [
    {
        "inputs": [
            {
                "internalType": "contract IOstiumRegistry",
                "name": "_registry",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotGov",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
                {
                    "internalType": "uint8",
                    "name": "",
                    "type": "uint8"
                }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "subtractedValue",
                "type": "uint256"
            }
        ],
        "name": "decreaseAllowance",
        "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "addedValue",
                "type": "uint256"
            }
        ],
        "name": "increaseAllowance",
        "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

ostium_trading_storage_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "target",
                "type": "address"
            }
        ],
        "name": "AddressEmptyCode",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "AddressInsufficientBalance",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "FailedInnerCall",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "InvalidInitialization",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            }
        ],
        "name": "NoOpenLimitOrder",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotCallbacks",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "NotEmptyIndex",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotGov",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "NotInitializing",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotManager",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotTrading",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotTradingOrCallbacks",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "NullAddr",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint8",
                "name": "bits",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "SafeCastOverflowedUintDowncast",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "SafeCastOverflowedUintToInt",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            }
        ],
        "name": "SafeERC20FailedOperation",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "WrongParams",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint64",
                "name": "version",
                "type": "uint64"
            }
        ],
        "name": "Initialized",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "MaxOpenInterestUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "MaxPendingMarketOrdersUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "MaxTradesPerPairUpdated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "claimFees",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "devFees",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            }
        ],
        "name": "firstEmptyOpenLimitIndex",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            }
        ],
        "name": "firstEmptyTradeIndex",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            }
        ],
        "name": "getOpenLimitOrder",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "targetPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "createdAt",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "lastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "enum IOstiumTradingStorage.OpenOrderType",
                        "name": "orderType",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.OpenLimitOrder",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint256",
                "name": "_index",
                "type": "uint256"
            }
        ],
        "name": "getOpenLimitOrderByIndex",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "targetPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "createdAt",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "lastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "enum IOstiumTradingStorage.OpenOrderType",
                        "name": "orderType",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.OpenLimitOrder",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            }
        ],
        "name": "getOpenLimitOrders",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "targetPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "createdAt",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "lastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "enum IOstiumTradingStorage.OpenOrderType",
                        "name": "orderType",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.OpenLimitOrder[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            }
        ],
        "name": "getOpenTrade",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "openPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.Trade",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            }
        ],
        "name": "getOpenTradeInfo",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "tradeId",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "oiNotional",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint32",
                        "name": "initialLeverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "tpLastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "slLastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "createdAt",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bool",
                        "name": "beingMarketClosed",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.TradeInfo",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            }
        ],
        "name": "getPairOpeningInterestInfo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            }
        ],
        "name": "getPendingOrderIds",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "getPendingRemoveCollateral",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "removeAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.PendingRemoveCollateral",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint256",
                "name": "latestPrice",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_leveragedPositionSize",
                "type": "uint256"
            },
            {
                "internalType": "uint32",
                "name": "leverage",
                "type": "uint32"
            },
            {
                "internalType": "bool",
                "name": "isBuy",
                "type": "bool"
            }
        ],
        "name": "handleOpeningFees",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "devFee",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "vaultFee",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            }
        ],
        "name": "hasOpenLimitOrder",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract IOstiumRegistry",
                "name": "_registry",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_usdc",
                "type": "address"
            }
        ],
        "name": "initialize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "maxPendingMarketOrders",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "maxTradesPerPair",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "openInterest",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "orderIndex",
                "type": "uint8"
            }
        ],
        "name": "openLimitOrderIds",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "openLimitOrdersCount",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "tradeIndex",
                "type": "uint8"
            }
        ],
        "name": "openTrades",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "collateral",
                "type": "uint256"
            },
            {
                "internalType": "uint192",
                "name": "openPrice",
                "type": "uint192"
            },
            {
                "internalType": "uint192",
                "name": "tp",
                "type": "uint192"
            },
            {
                "internalType": "uint192",
                "name": "sl",
                "type": "uint192"
            },
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint32",
                "name": "leverage",
                "type": "uint32"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "bool",
                "name": "buy",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "openTradesCount",
        "outputs": [
            {
                "internalType": "uint32",
                "name": "",
                "type": "uint32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "tradeIndex",
                "type": "uint8"
            }
        ],
        "name": "openTradesInfo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "oiNotional",
                "type": "uint256"
            },
            {
                "internalType": "uint32",
                "name": "initialLeverage",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "tpLastUpdated",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "slLastUpdated",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "createdAt",
                "type": "uint32"
            },
            {
                "internalType": "bool",
                "name": "beingMarketClosed",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "enum IOstiumTradingStorage.LimitOrder",
                "name": "orderType",
                "type": "uint8"
            }
        ],
        "name": "orderTriggerBlock",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "pairLimitOrders",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "collateral",
                "type": "uint256"
            },
            {
                "internalType": "uint192",
                "name": "targetPrice",
                "type": "uint192"
            },
            {
                "internalType": "uint192",
                "name": "tp",
                "type": "uint192"
            },
            {
                "internalType": "uint192",
                "name": "sl",
                "type": "uint192"
            },
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint32",
                "name": "leverage",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "createdAt",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "lastUpdated",
                "type": "uint32"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "enum IOstiumTradingStorage.OpenOrderType",
                "name": "orderType",
                "type": "uint8"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "bool",
                "name": "buy",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "pairTraders",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            }
        ],
        "name": "pairTradersArray",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "",
                "type": "address[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            }
        ],
        "name": "pairTradersCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "pairTradersId",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "pendingMarketCloseCount",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "pendingMarketOpenCount",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "pendingOrderIds",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            }
        ],
        "name": "pendingOrderIdsCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "registry",
        "outputs": [
            {
                "internalType": "contract IOstiumRegistry",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "reqID_pendingAutomationOrder",
        "outputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "enum IOstiumTradingStorage.LimitOrder",
                "name": "orderType",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "reqID_pendingMarketOrder",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "block",
                "type": "uint256"
            },
            {
                "internalType": "uint192",
                "name": "wantedPrice",
                "type": "uint192"
            },
            {
                "internalType": "uint32",
                "name": "slippageP",
                "type": "uint32"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "openPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.Trade",
                "name": "trade",
                "type": "tuple"
            },
            {
                "internalType": "uint16",
                "name": "percentage",
                "type": "uint16"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "reqID_pendingRemoveCollateral",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "removeAmount",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint256",
                "name": "_newMaxOpenInterest",
                "type": "uint256"
            }
        ],
        "name": "setMaxOpenInterest",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16[]",
                "name": "_indices",
                "type": "uint16[]"
            },
            {
                "internalType": "uint256[]",
                "name": "_newMaxOpenInterests",
                "type": "uint256[]"
            }
        ],
        "name": "setMaxOpenInterestArray",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_maxPendingMarketOrders",
                "type": "uint256"
            }
        ],
        "name": "setMaxPendingMarketOrders",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_maxTradesPerPair",
                "type": "uint256"
            }
        ],
        "name": "setMaxTradesPerPair",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            },
            {
                "internalType": "enum IOstiumTradingStorage.LimitOrder",
                "name": "_orderType",
                "type": "uint8"
            }
        ],
        "name": "setTrigger",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "targetPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "createdAt",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "lastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "enum IOstiumTradingStorage.OpenOrderType",
                        "name": "orderType",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.OpenLimitOrder",
                "name": "o",
                "type": "tuple"
            }
        ],
        "name": "storeOpenLimitOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "enum IOstiumTradingStorage.LimitOrder",
                        "name": "orderType",
                        "type": "uint8"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.PendingAutomationOrder",
                "name": "_automationOrder",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_orderId",
                "type": "uint256"
            }
        ],
        "name": "storePendingAutomationOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "block",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "wantedPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint32",
                        "name": "slippageP",
                        "type": "uint32"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "collateral",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint192",
                                "name": "openPrice",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "tp",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "sl",
                                "type": "uint192"
                            },
                            {
                                "internalType": "address",
                                "name": "trader",
                                "type": "address"
                            },
                            {
                                "internalType": "uint32",
                                "name": "leverage",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint16",
                                "name": "pairIndex",
                                "type": "uint16"
                            },
                            {
                                "internalType": "uint8",
                                "name": "index",
                                "type": "uint8"
                            },
                            {
                                "internalType": "bool",
                                "name": "buy",
                                "type": "bool"
                            }
                        ],
                        "internalType": "struct IOstiumTradingStorage.Trade",
                        "name": "trade",
                        "type": "tuple"
                    },
                    {
                        "internalType": "uint16",
                        "name": "percentage",
                        "type": "uint16"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.PendingMarketOrderV2",
                "name": "_order",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "_open",
                "type": "bool"
            }
        ],
        "name": "storePendingMarketOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "removeAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.PendingRemoveCollateral",
                "name": "request",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "storePendingRemoveCollateral",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "openPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.Trade",
                "name": "_trade",
                "type": "tuple"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "tradeId",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "oiNotional",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint32",
                        "name": "initialLeverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "tpLastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "slLastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "createdAt",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bool",
                        "name": "beingMarketClosed",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.TradeInfo",
                "name": "_tradeInfo",
                "type": "tuple"
            }
        ],
        "name": "storeTrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "totalOpenLimitOrders",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalOpenTradesCount",
        "outputs": [
            {
                "internalType": "uint32",
                "name": "",
                "type": "uint32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "transferUsdc",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            }
        ],
        "name": "unregisterOpenLimitOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_orderId",
                "type": "uint256"
            }
        ],
        "name": "unregisterPendingAutomationOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "_open",
                "type": "bool"
            }
        ],
        "name": "unregisterPendingMarketOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "unregisterPendingRemoveCollateral",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "_collateralToClose",
                "type": "uint256"
            }
        ],
        "name": "unregisterTrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            },
            {
                "internalType": "enum IOstiumTradingStorage.LimitOrder",
                "name": "_orderType",
                "type": "uint8"
            }
        ],
        "name": "unregisterTrigger",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "targetPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "createdAt",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "lastUpdated",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "enum IOstiumTradingStorage.OpenOrderType",
                        "name": "orderType",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.OpenLimitOrder",
                "name": "_o",
                "type": "tuple"
            }
        ],
        "name": "updateOpenLimitOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "_newSl",
                "type": "uint256"
            }
        ],
        "name": "updateSl",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "_index",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "_newTp",
                "type": "uint256"
            }
        ],
        "name": "updateTp",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "openPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.Trade",
                "name": "_t",
                "type": "tuple"
            }
        ],
        "name": "updateTrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "usdc",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

ostium_trading_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "AboveMaxAllowedCollateral",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "AlreadyMarketClosed",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "BelowMinLevPos",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "DelegatedActionFailed",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "ExposureLimits",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "InvalidInitialization",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "IsContract",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "IsDone",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "IsPaused",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            }
        ],
        "name": "MaxPendingMarketOrdersReached",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "MaxTradesPerPairReached",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NoDelegate",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "NoLimitFound",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "NoTradeFound",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "NoTradeToTimeoutFound",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "NotCloseMarketTimeoutOrder",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "NotDelegate",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotGov",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "NotInitializing",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotManager",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "NotOpenMarketTimeoutOrder",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "a",
                "type": "address"
            }
        ],
        "name": "NotTradesUpKeep",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            }
        ],
        "name": "NotYourOrder",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "NullAddr",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "index",
                "type": "uint16"
            }
        ],
        "name": "PairNotListed",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "RemoveAmountTooHigh",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint8",
                "name": "bits",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "SafeCastOverflowedUintDowncast",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "TriggerPending",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            }
        ],
        "name": "WaitTimeout",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "leverage",
                "type": "uint32"
            }
        ],
        "name": "WrongLeverage",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "WrongParams",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "WrongSL",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "WrongTP",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "enum IOstiumTradingStorage.LimitOrder",
                "name": "",
                "type": "uint8"
            }
        ],
        "name": "AutomationCloseOrderInitiated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "AutomationOpenOrderInitiated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "delegator",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "delegate",
                "type": "address"
            }
        ],
        "name": "DelegateAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "delegator",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "delegate",
                "type": "address"
            }
        ],
        "name": "DelegateRemoved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bool",
                "name": "done",
                "type": "bool"
            }
        ],
        "name": "Done",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint64",
                "name": "version",
                "type": "uint64"
            }
        ],
        "name": "Initialized",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "MarketCloseFailed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "MarketCloseOrderInitiated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "closePercentage",
                "type": "uint16"
            }
        ],
        "name": "MarketCloseOrderInitiatedV2",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "block",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "wantedPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint32",
                        "name": "slippageP",
                        "type": "uint32"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "collateral",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint192",
                                "name": "openPrice",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "tp",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "sl",
                                "type": "uint192"
                            },
                            {
                                "internalType": "address",
                                "name": "trader",
                                "type": "address"
                            },
                            {
                                "internalType": "uint32",
                                "name": "leverage",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint16",
                                "name": "pairIndex",
                                "type": "uint16"
                            },
                            {
                                "internalType": "uint8",
                                "name": "index",
                                "type": "uint8"
                            },
                            {
                                "internalType": "bool",
                                "name": "buy",
                                "type": "bool"
                            }
                        ],
                        "internalType": "struct IOstiumTradingStorage.Trade",
                        "name": "trade",
                        "type": "tuple"
                    }
                ],
                "indexed": False,
                "internalType": "struct IOstiumTradingStorage.PendingMarketOrder",
                "name": "order",
                "type": "tuple"
            }
        ],
        "name": "MarketCloseTimeoutExecuted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "block",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "wantedPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint32",
                        "name": "slippageP",
                        "type": "uint32"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "collateral",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint192",
                                "name": "openPrice",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "tp",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "sl",
                                "type": "uint192"
                            },
                            {
                                "internalType": "address",
                                "name": "trader",
                                "type": "address"
                            },
                            {
                                "internalType": "uint32",
                                "name": "leverage",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint16",
                                "name": "pairIndex",
                                "type": "uint16"
                            },
                            {
                                "internalType": "uint8",
                                "name": "index",
                                "type": "uint8"
                            },
                            {
                                "internalType": "bool",
                                "name": "buy",
                                "type": "bool"
                            }
                        ],
                        "internalType": "struct IOstiumTradingStorage.Trade",
                        "name": "trade",
                        "type": "tuple"
                    },
                    {
                        "internalType": "uint16",
                        "name": "percentage",
                        "type": "uint16"
                    }
                ],
                "indexed": False,
                "internalType": "struct IOstiumTradingStorage.PendingMarketOrderV2",
                "name": "order",
                "type": "tuple"
            }
        ],
        "name": "MarketCloseTimeoutExecutedV2",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            }
        ],
        "name": "MarketOpenOrderInitiated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "block",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "wantedPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint32",
                        "name": "slippageP",
                        "type": "uint32"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "collateral",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint192",
                                "name": "openPrice",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "tp",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "sl",
                                "type": "uint192"
                            },
                            {
                                "internalType": "address",
                                "name": "trader",
                                "type": "address"
                            },
                            {
                                "internalType": "uint32",
                                "name": "leverage",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint16",
                                "name": "pairIndex",
                                "type": "uint16"
                            },
                            {
                                "internalType": "uint8",
                                "name": "index",
                                "type": "uint8"
                            },
                            {
                                "internalType": "bool",
                                "name": "buy",
                                "type": "bool"
                            }
                        ],
                        "internalType": "struct IOstiumTradingStorage.Trade",
                        "name": "trade",
                        "type": "tuple"
                    }
                ],
                "indexed": False,
                "internalType": "struct IOstiumTradingStorage.PendingMarketOrder",
                "name": "order",
                "type": "tuple"
            }
        ],
        "name": "MarketOpenTimeoutExecuted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "block",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "wantedPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint32",
                        "name": "slippageP",
                        "type": "uint32"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "collateral",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint192",
                                "name": "openPrice",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "tp",
                                "type": "uint192"
                            },
                            {
                                "internalType": "uint192",
                                "name": "sl",
                                "type": "uint192"
                            },
                            {
                                "internalType": "address",
                                "name": "trader",
                                "type": "address"
                            },
                            {
                                "internalType": "uint32",
                                "name": "leverage",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint16",
                                "name": "pairIndex",
                                "type": "uint16"
                            },
                            {
                                "internalType": "uint8",
                                "name": "index",
                                "type": "uint8"
                            },
                            {
                                "internalType": "bool",
                                "name": "buy",
                                "type": "bool"
                            }
                        ],
                        "internalType": "struct IOstiumTradingStorage.Trade",
                        "name": "trade",
                        "type": "tuple"
                    },
                    {
                        "internalType": "uint16",
                        "name": "percentage",
                        "type": "uint16"
                    }
                ],
                "indexed": False,
                "internalType": "struct IOstiumTradingStorage.PendingMarketOrderV2",
                "name": "order",
                "type": "tuple"
            }
        ],
        "name": "MarketOpenTimeoutExecutedV2",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "value",
                "type": "uint16"
            }
        ],
        "name": "MarketOrdersTimeoutUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "MaxAllowedCollateralUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "OpenLimitCanceled",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "OpenLimitPlaced",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "indexed": False,
                "internalType": "uint192",
                "name": "newPrice",
                "type": "uint192"
            },
            {
                "indexed": False,
                "internalType": "uint192",
                "name": "newTp",
                "type": "uint192"
            },
            {
                "indexed": False,
                "internalType": "uint192",
                "name": "newSl",
                "type": "uint192"
            }
        ],
        "name": "OpenLimitUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bool",
                "name": "paused",
                "type": "bool"
            }
        ],
        "name": "Paused",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "removeAmount",
                "type": "uint256"
            }
        ],
        "name": "RemoveCollateralInitiated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "removeAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "reason",
                "type": "string"
            }
        ],
        "name": "RemoveCollateralRejected",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "indexed": False,
                "internalType": "uint192",
                "name": "newSl",
                "type": "uint192"
            }
        ],
        "name": "SlUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "topUpAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "newLeverage",
                "type": "uint32"
            }
        ],
        "name": "TopUpCollateralExecuted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tradeId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "indexed": False,
                "internalType": "uint192",
                "name": "newTp",
                "type": "uint192"
            }
        ],
        "name": "TpUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "value",
                "type": "uint16"
            }
        ],
        "name": "TriggerTimeoutUpdated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "_msgSender",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "cancelOpenLimitOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "enum IOstiumTradingStorage.LimitOrder",
                "name": "orderType",
                "type": "uint8"
            }
        ],
        "name": "checkNoPendingTrigger",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "checkNoPendingTriggers",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "uint16",
                "name": "closePercentage",
                "type": "uint16"
            }
        ],
        "name": "closeTradeMarket",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_order",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "retry",
                "type": "bool"
            }
        ],
        "name": "closeTradeMarketTimeout",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "call_data",
                "type": "bytes"
            }
        ],
        "name": "delegatedAction",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "delegator",
                "type": "address"
            }
        ],
        "name": "delegations",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "done",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IOstiumTradingStorage.LimitOrder",
                "name": "orderType",
                "type": "uint8"
            },
            {
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "priceTimestamp",
                "type": "uint256"
            }
        ],
        "name": "executeAutomationOrder",
        "outputs": [
            {
                "internalType": "enum IOstiumTrading.AutomationOrderStatus",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract IOstiumRegistry",
                "name": "_registry",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_maxAllowedCollateral",
                "type": "uint256"
            },
            {
                "internalType": "uint16",
                "name": "_marketOrdersTimeout",
                "type": "uint16"
            },
            {
                "internalType": "uint16",
                "name": "_triggerTimeout",
                "type": "uint16"
            }
        ],
        "name": "initialize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isDone",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isPaused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "marketOrdersTimeout",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "maxAllowedCollateral",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "collateral",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint192",
                        "name": "openPrice",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "tp",
                        "type": "uint192"
                    },
                    {
                        "internalType": "uint192",
                        "name": "sl",
                        "type": "uint192"
                    },
                    {
                        "internalType": "address",
                        "name": "trader",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "leverage",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint16",
                        "name": "pairIndex",
                        "type": "uint16"
                    },
                    {
                        "internalType": "uint8",
                        "name": "index",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bool",
                        "name": "buy",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IOstiumTradingStorage.Trade",
                "name": "t",
                "type": "tuple"
            },
            {
                "internalType": "enum IOstiumTradingStorage.OpenOrderType",
                "name": "orderType",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "slippageP",
                "type": "uint256"
            }
        ],
        "name": "openTrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_order",
                "type": "uint256"
            }
        ],
        "name": "openTradeMarketTimeout",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "pause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "registry",
        "outputs": [
            {
                "internalType": "contract IOstiumRegistry",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "removeAmount",
                "type": "uint256"
            }
        ],
        "name": "removeCollateral",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "removeDelegate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "delegate",
                "type": "address"
            }
        ],
        "name": "setDelegate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "setMarketOrdersTimeout",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "setMaxAllowedCollateral",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "setTriggerTimeout",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "topUpAmount",
                "type": "uint256"
            }
        ],
        "name": "topUpCollateral",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "triggerTimeout",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "uint192",
                "name": "price",
                "type": "uint192"
            },
            {
                "internalType": "uint192",
                "name": "tp",
                "type": "uint192"
            },
            {
                "internalType": "uint192",
                "name": "sl",
                "type": "uint192"
            }
        ],
        "name": "updateOpenLimitOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "uint192",
                "name": "newSl",
                "type": "uint192"
            }
        ],
        "name": "updateSl",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "pairIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            },
            {
                "internalType": "uint192",
                "name": "newTp",
                "type": "uint192"
            }
        ],
        "name": "updateTp",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]  # ABI of your deployed contract
