from typing import TypedDict, Annotated, List, Optional
from semantic_kernel.functions import kernel_function

class LightModel(TypedDict):
   id: int
   name: str
   is_on: bool | None
   brightness: int | None
   hex: str | None

class LightsPlugin:
   lights: list[LightModel] = [
      {"id": 1, "name": "Table Lamp", "is_on": False, "brightness": 100, "hex": "FF0000"},
      {"id": 2, "name": "Porch light", "is_on": False, "brightness": 50, "hex": "00FF00"},
      {"id": 3, "name": "Chandelier", "is_on": True, "brightness": 75, "hex": "0000FF"},
   ]

   @kernel_function
   async def get_lights(self) -> List[LightModel]:
      """Gets a list of lights and their current state."""
      return self.lights

   @kernel_function
   async def get_state(
      self,
      id: Annotated[int, "The ID of the light"]
   ) -> Optional[LightModel]:
      """Gets the state of a particular light."""
      for light in self.lights:
         if light["id"] == id:
               return light
      return None

   @kernel_function
   async def change_state(
      self,
      id: Annotated[int, "The ID of the light"],
      new_state: LightModel
   ) -> Optional[LightModel]:
      """Changes the state of the light."""
      for light in self.lights:
         if light["id"] == id:
               light["is_on"] = new_state.get("is_on", light["is_on"])
               light["brightness"] = new_state.get("brightness", light["brightness"])
               light["hex"] = new_state.get("hex", light["hex"])
               return light
      return None
