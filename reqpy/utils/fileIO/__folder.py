# from pathlib import Path


# def get_dirList(
#     rootdir: Path,
#     sub_conf: dict
#     ) -> <tuple(Path):
#     """ Provide a tuple of Path based on a dict that contains dictionary with name and sub field (see example)

#     dictionnary example:
#     folder_structure ={
#         'name':'requirements',
#         'sub': [{
#             'name':'links',
#             'sub':[]
#         },{
#             'name':'analysis',
#             'sub':[]
#         }]
#     }
#     """
            
#             def get_dir(
#                 current_dir:Path,
#                 sub_folder_dict : dict,
#                 result : list[Path] = None
#                 ) -> list[Path]
            
#                 if result == None:
#                     result = [current_dir / sub_folder_dict['name']]
                                        
#                     for sub in sub_folder_dict['sub']:
#                         result.append(get_dir(
#                         current_dir = current_dir / sub_folder_dict['name'],
#                         sub_folder_dict = sub
#                         result = result
#                         ))
                        
                
#             curr_dir = current_dir / sub_conf['name']
#             # create dir
#             print("create:", str(curr_dir))
#             curr_dir.mkdir(parents=True, exist_ok=True)
#             for sub in sub_conf['sub']:
#                 create_dir(curr_dir, sub)
