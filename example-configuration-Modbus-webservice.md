# Exemple de configuration d'une invseobox sur le logiciel inviseo
Vous trouverez ci-dessous un exemple concret de configuration d'une inviseobox au format `JSON`.
Cet exemple est tiré du logiciel `Inviseo` et de notre client `Les chanvres de l'atlantique`.

## Liste des inviseobox, de leurs appreils et mesures
```json
[
    {
        "_id": "6679791b84803b31206f502b",
        "name": "Inviséobox 1",
        "site": "6655d59ffe6296f77480cee0",
        "devices": [
            {
                "_id": "6679814384803b31206fbae4",
                "name": "Capteur hygrométrie mur",
                "status": "dead",
                "worker": "6679791b84803b31206f502b",
                "communication": {
                    "protocol": "WebService",
                    "configuration": {
                        "url": "http://192.168.2.34/"
                    }
                },
                "measurements": [
                    {
                        "name": "Mesure 1 (Chambre froide)",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "hum1"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "%",
                        "_id": "6679814384803b31206fbae5"
                    },
                    {
                        "name": "Mesure 2",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "hum2"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "%",
                        "_id": "6679814384803b31206fbae6"
                    },
                    {
                        "name": "Mesure 3",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "hum3"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "%",
                        "_id": "6679814384803b31206fbae7"
                    },
                    {
                        "name": "Mesure 4",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "hum4"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "%",
                        "_id": "6679814384803b31206fbae8"
                    },
                    {
                        "name": "Mesure 5",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "hum5"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "%",
                        "_id": "6679814384803b31206fbae9"
                    },
                    {
                        "name": "Mesure 6 (extérieur)",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "hum6"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "%",
                        "_id": "6679814384803b31206fbaea"
                    }
                ],
                "createdAt": "2024-06-24T14:22:59.280Z",
                "updatedAt": "2024-06-24T14:22:59.287Z",
                "__v": 0
            },
            {
                "_id": "667981b484803b31206fbaf0",
                "name": "Capteur température mur",
                "status": "dead",
                "worker": "6679791b84803b31206f502b",
                "communication": {
                    "protocol": "WebService",
                    "configuration": {
                        "url": "http://192.168.2.35/"
                    }
                },
                "measurements": [
                    {
                        "name": "Mesure 1 (Chambre froide)",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "temp1"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "°C",
                        "_id": "667981b484803b31206fbaf1"
                    },
                    {
                        "name": "Mesure 2",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "temp2"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "°C",
                        "_id": "667981b484803b31206fbaf2"
                    },
                    {
                        "name": "Mesure 3",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "temp3"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "°C",
                        "_id": "667981b484803b31206fbaf3"
                    },
                    {
                        "name": "Mesure 4",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "temp4"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "°C",
                        "_id": "667981b484803b31206fbaf4"
                    },
                    {
                        "name": "Mesure 5",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "temp5"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "°C",
                        "_id": "667981b484803b31206fbaf5"
                    },
                    {
                        "name": "Mesure 6 (extérieur)",
                        "status": "dead",
                        "usage": [],
                        "configuration": {
                            "parameters": {
                                "key": "temp6"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "°C",
                        "_id": "667981b484803b31206fbaf6"
                    }
                ],
                "createdAt": "2024-06-24T14:24:52.318Z",
                "updatedAt": "2024-06-24T14:24:52.323Z",
                "__v": 0
            },
            {
                "_id": "668c017b3ac366396efc0d80",
                "name": "Compteur Modbus",
                "status": "dead",
                "reference": "236-9298",
                "worker": "6679791b84803b31206f502b",
                "communication": {
                    "protocol": "Modbus",
                    "mode": "RTU",
                    "type": "RS-485",
                    "configuration": {
                        "port": "/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",
                        "stopbits": 1,
                        "bytesize": 8,
                        "parity": "N",
                        "baudrate": 9600
                    }
                },
                "measurements": [
                    {
                        "name": "Puissance chambre froide stockage",
                        "type": "puissance",
                        "energy": "électricité",
                        "status": "dead",
                        "usage": [
                            "process"
                        ],
                        "configuration": {
                            "parameters": {
                                "register": "0x04",
                                "address": 52,
                                "slave": 2,
                                "count": 2,
                                "byte_order": "3-2-1-0",
                                "value_class": "FLOAT32"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "W",
                        "_id": "668c017b3ac366396efc0d81"
                    },
                    {
                        "name": "Consommation chambre froide stockage",
                        "type": "consommation",
                        "energy": "électricité",
                        "status": "dead",
                        "usage": [
                            "process"
                        ],
                        "configuration": {
                            "parameters": {
                                "register": "0x04",
                                "address": 342,
                                "slave": 2,
                                "count": 2,
                                "byte_order": "3-2-1-0",
                                "value_class": "FLOAT32"
                            },
                            "response_format": [
                                "diff"
                            ]
                        },
                        "unit": "kWh",
                        "_id": "668c017b3ac366396efc0d82"
                    },
                    {
                        "name": "Consommation chambre froide SAS",
                        "type": "consommation",
                        "energy": "électricité",
                        "status": "dead",
                        "usage": [
                            "process"
                        ],
                        "configuration": {
                            "parameters": {
                                "register": "0x04",
                                "address": 342,
                                "slave": 3,
                                "count": 2,
                                "byte_order": "3-2-1-0",
                                "value_class": "FLOAT32"
                            },
                            "response_format": [
                                "diff"
                            ]
                        },
                        "unit": "kWh",
                        "_id": "668c017b3ac366396efc0d83"
                    },
                    {
                        "name": "Puissance chambre froide SAS",
                        "type": "puissance",
                        "energy": "électricité",
                        "status": "dead",
                        "usage": [
                            "process"
                        ],
                        "configuration": {
                            "parameters": {
                                "register": "0x04",
                                "address": 52,
                                "slave": 3,
                                "count": 2,
                                "byte_order": "3-2-1-0",
                                "value_class": "FLOAT32"
                            },
                            "response_format": [
                                "min",
                                "max",
                                "avg"
                            ]
                        },
                        "unit": "W",
                        "_id": "668c017b3ac366396efc0d84"
                    }
                ],
                "createdAt": "2024-07-08T15:10:51.569Z",
                "updatedAt": "2024-07-08T15:10:51.573Z",
                "__v": 0
            }
        ],
        "token": "24a0e1fdf48991683a91e0164979a5416c4754465d730443f59a51166ad208dd",
        "createdAt": "2024-06-24T13:48:11.571Z",
        "updatedAt": "2024-06-24T13:48:11.575Z",
        "__v": 0,
        "interval": 1800
    }
]
```

## Interface en typescript
par mesure de comodité, voici également les interfaces génériques en `typescript`. Mais elles peuvent être réécrites dans n'importe quelle langage.
J'ai pris soin d'y ajouter des commnetaire et la JSDoc.
```typescript
/**
 * Configuration représente les paramètres techniques spécifiques nécessaires à la communication 
 * entre un appareil installés chez le client (box et capteur) et le système (initialement inviseo)
 */
interface Configuration {
  /** URL utilisée pour établir la communication avec l'appareil (dans le cas d'un capteur en qui communique en http). */
  url?: string;
  
  /** Paramètres envoyés à l'appareil pour récupérer les données (exemple : clé, registre). */
  parameters?: Record<string, string>;
  
  /** Format de la réponse retournée par l'appareil (exemple : min, max, avg ou diff). */
  response_format?: string[];
  
  /** Port série pour les communications Modbus (exemple : /dev/serial/...). */
  port?: string;
  
  /** Nombre de bits de stop pour la communication série. */
  stopbits?: number;
  
  /** Nombre de bits de données pour la communication série. */
  bytesize?: number;
  
  /** Parité utilisée pour la communication (exemple : N = None, E = Even ou O = Odd). */
  parity?: string;
  
  /** Vitesse de transmission (baudrate) en bits par seconde. */
  /** nous avons remarqué que le baudrate 9200 etait idéal pour notre communication */
  baudrate?: number;
  
  /** Registre utilisé pour accéder aux données via Modbus. */
  register?: string;
  
  /** Adresse du registre (emplacement mémoire du capteur Modbus). */
  address?: number;
  
  /** Identifiant de l'esclave dans une communication Modbus (multi-appareils). */
  slave?: number;
  
  /** Nombre de registres à lire. */
  count?: number;
  
  /** Ordre des octets utilisé pour interpréter les valeurs binaires. */
  byte_order?: string;
  
  /** Type de valeur lue (exemple : FLOAT32 pour une valeur décimale). */
  value_class?: string;
}

/**
 * Communication décrit comment un appareil communique avec le système.
 */
interface Communication {
  /** Protocole de communication utilisé (exemple : WebService, Modbus). */
  protocol: string;
  
  /** Configuration détaillée pour établir la connexion. */
  configuration: Configuration;
  
  /** Mode de communication (uniquement pour Modbus, ex : RTU ou TCP). */
  mode?: string;
  
  /** Type de connexion physique (uniquement pour Modbus, ex : RS-485). */
  type?: string;
}

/**
 * Measurement (Mesure) représente une donnée collectée par un appareil, comme la température, l'humidité, la puissance ou encore la consommation.
 */
interface Measurement {
  /** Identifiant unique de la mesure. */
  _id: string;
  
  /** Nom de la mesure (exemple : "Température extérieure"). */
  name: string;
  
  /** Statut de la mesure (exemple : "active", "dead"). */
  /** Définit si la mesure a pu être relever ou non */
  status: string;
  
  /** Liste d'usages spécifiques pour cette mesure (exemple : ["process"]). */
  usage: string[];
  
  /** Configuration spécifique pour cette mesure, incluant les paramètres nécessaires à la collecte des données. */
  configuration: Configuration;
  
  /** Unité de la mesure (exemple : "°C", "%"). */
  unit: string;
  
  /** Type de la mesure (optionnel, exemple : "puissance", "consommation"). */
  type?: string;
  
  /** Type d'énergie mesurée (optionnel, exemple : "électricité"). */
  energy?: string;
}

/**
 * Device (Appareil) représente un appareil connecté au système, capable de fournir des mesures et possedant au moins une mesure.
 */
interface Device {
  /** Identifiant unique de l'appareil. */
  _id: string;
  
  /** Nom de l'appareil (exemple : "Capteur de température"). */
  name: string;
  
  /** Statut de l'appareil (exemple : "active", "dead"). */
  /** Idem pour les mesures. Definit si l'appareil a pu etre consulté */
  status: string;
  
  /** Référence à l'identifiant du "worker" (inviseobox) qui gère cet appareil. */
  worker: string;
  
  /** Informations sur la communication avec l'appareil. */
  communication: Communication;
  
  /** Liste des mesures disponibles sur cet appareil. */
  measurements: Measurement[];
  
  /** Référence optionnelle de l'appareil (utile pour la documentation ou le suivi externe). */
  reference?: string;
  
  /** Date de création de cet appareil dans le système. */
  createdAt: string;
  
  /** Dernière mise à jour des informations de l'appareil. */
  updatedAt: string;
  
  /** Version du document dans la base de données (généré automatiquement). */
  __v: number;
}

/**
 * Site (batiment) représente un site ou une unité contenant un ensemble d'appareils connectés.
 */
interface Site {
  /** Identifiant unique du site. */
  _id: string;
  
  /** Nom du site (exemple : "Usine de production"). */
  name: string;
  
  /** Identifiant du site parent ou organisation associé. */
  site: string;
  
  /** Liste des appareils connectés sur ce site. */
  devices: Device[];
  
  /** Jeton de sécurité pour accéder aux données du site. */
  token: string;
  
  /** Date de création du site dans le système. */
  createdAt: string;
  
  /** Dernière mise à jour des informations du site. */
  updatedAt: string;
  
  /** Version du document dans la base de données (généré automatiquement). */
  __v: number;
  
  /** Intervalle en secondes pour collecter les données des appareils. */
  interval: number;
}
```

## inserer des fields, format de requete
Dans le logiciel inviseo, la box contacte une url specifique pour inserer des champs en "masse".
Voici un exemple de requete envoyé par la box au format JSON.
Pour information, le `token` est un identifiant unique qui identifie (autre que l'id) une box auprès du logiciel inviseo.
```JSON
{
  "token": "exemple_de_token",
  "fields": [
    {
      "measurement": "64a2f123e4b0c1234567890a",
      "value": {
        "min": "12.3",
        "max": "25.7",
        "avg": "18.4",
        "diff": "13.4"
      },
      "timestamp": "2024-12-24T15:30:00Z"
    },
    {
      "measurement": "64a2f123e4b0c1234567890b",
      "value": {
        "min": "15.0",
        "max": "30.0",
        "avg": "22.0",
        "diff": "15.0"
      },
      "timestamp": "2024-12-24T14:15:00Z"
    }
  ]
}
```
Vous pouvez retrouver le la fonction qui accepte cette requete ici [Logiciel inviseo, bulk insert](https://github.com/Inviseo/inviseo/blob/63ee1658bf3a7da74076d6f7547116239c01b4bb/server/src/api/controllers/fieldController.js#L55)
Attention cependant, vous devez avoir les droit d'acces au dépôt de code `Inviseo` pour consulter ce lien.
