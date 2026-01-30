Status: work in progress
Goal: Build a 2D platformer level editor and game that runs the levels

# current features:
  - Level editor
  - player movement and collisions
  - basic enemy behavior(still buggy)
  - uses already set game tiles to make custom levels

# Known limitations:
  -No win/lose conditions yet
  -No death
  -No particle system
  -Enemy movement still buggy
  -game loop still expanded
  -No notification when file is saved/loaded


  ## How to use level editor:
  -W/A/S/D to move level around
  -SHIFT +A/D to change to different game assets
  -press and hold G to be able to place items offgrid/free placement(e.g Trees and flowers)
  -left mouse button to delete single item
  -SHIFT + left mouse button click and mouse movement to use mass selector:
            - selector + T to fix layout
            - selector + q for mass deletion(delete multiple items)
  ******NB!! save files to LEVELS Folder*****

  -You need to set player spawn point and enemy spawn point(They are part of the assets, use SHIFT +A/D to change to different game assets)

  ## How to use game
  -level number corresponds to position of level in file
        e.g) level 1 is the first file in LEVELS
  -W/A/S/D to move player and play level

  
  
