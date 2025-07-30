# ######################################################################################################################
#  MSO Copyright (c) 2025 by Charles L Beyor                                                                           #
#  is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.                          #
#  To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/                            #
#                                                                                                                      #
#  Unless required by applicable law or agreed to in writing, software                                                 #
#  distributed under the License is distributed on an "AS IS" BASIS,                                                   #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                            #
#  See the License for the specific language governing permissions and                                                 #
#  limitations under the License.                                                                                      #
#                                                                                                                      #
#  Gitlab: https://github.com/chuckbeyor101/MSO-Mongo-Schema-Object-Library                                            #
# ######################################################################################################################

def parse_schema(schema, name='Root'):
    classes = {}
    properties = schema.get('properties', {})
    for prop_name, prop_info in properties.items():
        if prop_info.get('type') == 'object':
            nested_class_name = f"{name}_{prop_name.capitalize()}"
            nested_classes = parse_schema(prop_info, nested_class_name)
            classes.update(nested_classes)
    classes[name] = schema
    return classes