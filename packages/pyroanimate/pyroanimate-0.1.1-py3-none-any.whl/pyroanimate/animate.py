import asyncio
from pyrogram import Client, types
from time import sleep
class Animate:
    def __init__(self, client: Client,delay=0.3,sync=True):
        self.client=client
        self.animations=self.load_animations()
        self.delay=delay
        self.sync=sync
    

    def add_animations(self,id,frames):
        self.animations[id]=frames
        if not isinstance(frames,list):
            raise ValueError("Frames must be a list of strings")
        return id

    def load_animations(self) -> dict:
        animations={

        }
        return animations


    def get_animation(self,id):
        animations=self.animations
        if id not in animations:
            raise ValueError(f"No animation found with id '{id}'.")
        return animations[id]

    def edit_delay(self,delay):
        if not isinstance(delay,(int,float)):
            raise ValueError("Delay must be a float")
        self.delay=delay
        return delay

    def run(self,chat_id,default,frames=None,animation_id=None):
        if self.sync==True:
            self._sync_run(chat_id,default,frames,animation_id)
        else:
            asyncio.run(self._async_run(chat_id, default, frames, animation_id))
            
    def _sync_run(self,chat_id,default,frames,animation_id):
        if default:
            if not animation_id:
                raise ValueError("If 'default' is True, you must provide an 'animation_id'.")
            else:
                frames=self.get_animation(animation_id)
        else:
            if not frames:
                raise ValueError("If 'default' is False, you must provide a list of 'frames'")
            
        app=self.client
        msg=app.send_message(chat_id,frames[0]) #type: types.Message
        sleep(self.delay)
        for frame in frames[1:]:
            msg.edit(frame)
            sleep(self.delay)

    async def _async_run(self,chat_id,default,frames,animation_id):
        if default:
            if not animation_id:
                raise ValueError("If 'default' is True, you must provide an 'animation_id'.")
            else:
                frames=self.get_animation(animation_id)
        else:
            if not frames:
                raise ValueError("If 'default' is False, you must provide a list of 'frames'")
            
        app=self.client
        msg= await app.send_message(chat_id,frames[0]) #type: types.Message         
        await asyncio.sleep(self.delay)
        for frame in frames[1:]:
            await msg.edit(frame)
            await asyncio.sleep(self.delay)

    