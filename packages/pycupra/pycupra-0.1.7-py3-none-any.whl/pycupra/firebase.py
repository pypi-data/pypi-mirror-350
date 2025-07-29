import logging
import asyncio
import os
import json
import string
import secrets

from .firebase_messaging import FcmPushClient, FcmRegisterConfig

from .const import (
    FCM_PROJECT_ID,
    FCM_API_KEY,
    FCM_APP_ID
)

_LOGGER = logging.getLogger(__name__)

class Firebase():
    def __init__(self):
        self._pushClient = None

    async def firebaseStart(self, onNotificationFunc, firebaseCredentialsFileName, brand='cupra'): 
        """ Starts the firebase cloud messaging receiver """
        try:
            loop = asyncio.get_running_loop()
            credentials = await loop.run_in_executor(None, readFCMCredsFile, firebaseCredentialsFileName)
            #credentials = readFCMCredsFile(firebaseCredentialsFileName)
            if credentials == {}:
                credentials =''

            fcm_project_id=FCM_PROJECT_ID
            fcm_app_id=FCM_APP_ID[brand]
            fcm_api_key=FCM_API_KEY
            chars = string.ascii_letters + string.digits
            fcmMessageSenderId = ''.join(secrets.choice(chars) for i in range(16)) 
            fcmMessageSenderId= 'fxpWQ_'+fcmMessageSenderId

            fcm_config = FcmRegisterConfig(fcm_project_id, fcm_app_id, fcm_api_key, fcmMessageSenderId)
            self._pushClient = FcmPushClient(onNotificationFunc, fcm_config, credentials, onFCMCredentialsUpdated)
            fcm_token = await self._pushClient.checkin_or_register(firebaseCredentialsFileName)
            _LOGGER.debug(f'Firebase.checkin_or_register() returned a token:{fcm_token}')
            await self._pushClient.start()
            await asyncio.sleep(5)
            return self._pushClient.is_started()
        except Exception as e:
            _LOGGER.error('Error in firebaseStart. Error: {e}')
            return False

    async def firebaseStop(self): 
        """ Stops the firebase cloud messaging receiver """
        try:
            await self._pushClient.stop()
            #await asyncio.sleep(5)
            self._pushClient = None
            return True
        except Exception as e:
            _LOGGER.error('Error in firebaseStop. Error: {e}')
            return False

def readFCMCredsFile(credsFile):
    """ Reads the firebase cloud messaging credentials from file"""
    try:
        if os.path.isfile(credsFile):
            with open(credsFile, "r") as f:
                credString=f.read()
            f.close()
            creds=json.loads(credString)
            return creds
        else:
            _LOGGER.debug(f'{credsFile} not found.')
            return {}
    except Exception as e:
        _LOGGER.warning('readFCMCredsFile() not successful. Error: {e}')
        return ''

def writeFCMCredsFile(creds, firebaseCredentialsFileName):
    """ Saves the firebase cloud messaging credentials to a file for future use """
    try:
        with open(firebaseCredentialsFileName, "w") as f:
            f.write(json.dumps(creds))
        f.close()
    except Exception as e:
        _LOGGER.warning(f'writeFCMCredsFile() not successful. Error: {e}')
    
async def onFCMCredentialsUpdated(creds, firebaseCredentialsFileName):
    """ Is called from firebase-messaging package """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, writeFCMCredsFile, creds, firebaseCredentialsFileName)
    #writeFCMCredsFile(creds, firebaseCredentialsFileName)
    
