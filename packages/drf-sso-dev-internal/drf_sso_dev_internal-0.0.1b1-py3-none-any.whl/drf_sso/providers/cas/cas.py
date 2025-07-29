import requests
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)

class CAS:
    def __init__(self, conf: Path | dict):
        if isinstance(conf, Path):
            with open(conf, 'r') as file:
                self._load_conf(json.load(file))
        else:
            self._load_conf(conf)
            
    def _load_conf(self, conf: dict):
        self.login_url = conf['login_url']
        self.validate_url = conf['validate_url']
        self.service_url = conf['service_url']
        
    def get_login_url(self):
        return f"{self.login_url}?service={self.service_url}"
    
    def validate_ticket(self, ticket = None):
        try:
            if ticket is None:
                raise Exception("CAS Ticket is invalid.")
            
            params = {
                'ticket': ticket,
                'service': self.service_url
            }
            response = requests.get(self.validate_url, params=params, timeout=5)
            response.raise_for_status()

            root = ET.fromstring(response.text)
            ns = {'cas': 'http://www.yale.edu/tp/cas'}

            auth_success = root.find('.//cas:authenticationSuccess', ns)
            if auth_success is None:
                raise Exception("CAS Auth failed.")
            
            user = auth_success.find('cas:user', ns).text
            attributes = auth_success.find('cas:attributes', ns)
            
            atr_dict = {}
            for attr in attributes:
                tag = attr.tag.split("}")[-1]
                if tag in atr_dict:
                    if isinstance(atr_dict[tag], list):
                        atr_dict[tag].append(attr.text)
                    else:
                        atr_dict[tag] = [atr_dict[tag], attr.text]
                else:
                    atr_dict[tag] = attr.text
                    
            return (user, atr_dict)

        except Exception as e:
            logger.error(e)
            return (None, None)