# DJANGO FINAL PROJECT
## **Project name**: Spotifi
## **Project description**: Spotifi is a digital music that gives you access to millions of songs and other content from creators all over the world. Basic functions such as playing music are totally free.
##    There will be more 9 entities in database, starting from just user and ended with playlists. Every user can listen, put like, filter and order music by self desire. User also can change profile image, and username. Admin is like user but have more permissions like add music or remove it. 
##     And there are not all. There will be a algorithm_bot_v001 which will make personal/general playlists for 24h every day. It just ran by table user_category_count, which will count how many times user listened some category
##     For security of all user and musics there is jwt authorization with access token and refresh token. Access token will expire in 30 min and refresh for day. 
# Installing
## Step 1: Clone project to your local enviroment -> git clone <link>
## Step 2: Create and run docker container -> docker-compose up -d --build
## Step 3: Create and run migrations -> make migrate-create name=api
## Step 4(Optionaly): Create superuser if need
## Step 5: Use it