# Food_Delivery

### 系統簡介:

- Demo影片連結：https://u.pcloud.link/publink/show?code=XZ7EO70Ztm7odLEpVfym0pUO5r6v5JfeNOmX

- 本系統提供以下功能，包含會員、餐廳列表、購物車、訂單等功能供使用者使用
    
    - 會員功能

        - 包含註冊、登入等功能，使用Redis進行Session cookie驗證

    - 餐廳菜單
        
        - 登入後可查看現有所有的餐廳列表、餐廳地址、菜單連結

        - 點進餐廳菜單即可點餐，點選數量並加上備註後，放入購物車，可點左上角「購物車」查詢
    
    - 購物車
        
        - 使用者進入購物車，可以查看購物車明細，包含餐廳、菜名、數量、單價、總價、備註等

        - 購物車最下面會自動使用者算出購物車所有明細合計價格

        - 使用者可點選按鈕：清空購物車、結帳、
            
            - 「清空購物車」會直接清空購物車所有明細
            
            - 「結帳」則會將購物車所有產品依照選定的付款方式，送出成一筆訂單，並清空購物車
            
            - 可點左上角「訂單列表」查詢訂單
    
    - 訂單
        
        - 點進「訂單列表」可查詢所有未被取消的訂單，包含訂購時間、總金額、付款方式、訂單明細

        - 點進訂單明細則看查看該筆訂單的產品明細，包含餐廳、菜名、數量、單價、總價、備註等

        - 點選取消訂單該筆訂單則會被取消，無法在「訂單列表」被查詢，但仍保存在資料庫


### 程式進入點:
    python main.py

### 使用方式:
- 需要先建立資料庫帳號密碼和Redis的連線，在啟用服務
- localhost:8000/Login.html: 登入頁面
- localhost:8000/Register.html: 註冊頁面
- localhost:8000/restaurant: 餐廳列表頁面
- localhost:8000/restaurant/{restaurant_id}: 指定餐廳的菜單頁面，可進行點餐
- localhost:8000/cart_item/: 購物車的頁面，有總金額和明細，可選擇付款方式進行結帳
- localhost:8000/order/: 訂單頁面，可查看未被取消的所有訂單
- localhost:8000/order/{order_id}: 訂單明細頁面，可查看訂單明細，也可取消訂單
- localhost:8000/docs: 產生API的文件

## 文件路徑圖、程式簡介：
    main.py
    Dockerfile
    data.sql
    requirements.txt
    static/
    templates/
    app/
        dao/
        env/
        routers/
        tools/

- main.py
    
    - 執行主程式，會啟動一個API引擎並部署

- Dockerfile
    
    - 建立docker的image的設定檔

- data.sql
    
    - sql檔

- requirements.txt
    
    - 所需要安裝的套件版本

- app
    - dao/
        
        - 處理和資料庫連接的資料層
    
    - env/
        
        - 存放可自定義的環境變數、資料庫路徑和密碼等
    
    - routers/
        
        - controller層，接收API傳的參數，以及API的處理   
    
    - tools/
        
        - 可能會重複使用到函式，主要處理session cookie驗證


- templates/
    
    - 存放每個網頁的HTML的檔案

- static/
    
    - 存放CSS和JavaScript的檔案，主要用Ajax負責處理前後端的串接

    
# 程式細節介紹

## `user`
### 用途： 
- 處理會員註冊、登入等功能

## `restaurant`
### 用途： 
- 處理餐廳以及菜單的功能
- restaurant/: 可取得餐廳的列表
- restaurant/{restaurant_id}: 可取得該餐廳的菜單並進行點餐

## `cart_item`
### 用途： 
- 處理購物車的功能，包括計算購物車總金額，以及將購物車資料送出成訂單

## `order`
### 用途： 
- 處理訂單、訂單明細、取消訂單等功能
- order/: 可取得所有訂單的表格
- order/{order_id}: 可取得該筆訂單的明細

## `tools.go`
### 用途：
  - 可能會被重複利用的函數，處理authentication的驗證


## `config.py`
### 用途： 
- 存放可自定義的環境變數、資料庫路徑和密碼等


# `DB_Schema` 
- DB的設計和table以及各個欄位類型及描述

    - Cart_item: 單筆的購物車明細
        - cart_item_id (int): 購物車單筆明細
        - member_id (varchar): 使用者id
        - food_id (int): 菜的id
        - food_name (varchar): 菜名
        - food_price (int): 菜的單價
        - food_quantity (int): 該筆明細菜的數量
        - food_remark (varchar): 客製化的備註
        - cart_item_price (int): 該筆明細的總價, 單價*數量
        - restaurant_name (varchar): 菜為哪間餐廳製作
    - Food
        - food_id (int): 菜的id
        - restaurant_id (int): 菜為哪間餐廳製作
        - food_name (varchar): 每道菜的菜名
        - food_price (varchar): 菜的單價
    - Order
        - order_id (int unsigned): 訂單的id
        - member_id (varchar): 使用者id
        - total_price (varchar): 訂單的總價
        - payment_name (varchar): 付款方式
        - order_status (varchar): 訂單狀態(送出/取消)
        - book_time (datetime): 下訂時間
    - Order_item
        - order_item_id (int): 訂單單筆明細
        - order_id (int): 訂單的id
        - food_id (int): 菜的id
        - food_name (varchar): 菜名
        - food_price (int): 菜的單價
        - food_quantity (int): 該筆明細菜的數量
        - food_remark (varchar): 客製化的備註
        - restaurant_name (varchar): 菜為哪間餐廳製作
        - order_item_price (int): 該筆明細的總價, 單價*數量
    - Payment
        - payment_id (int): 付款方式id
        - payment_name (varchar): 付款方式名稱
    - Restaurant
        - restaurant_id (int): 餐廳id
        - restaurant_name (varchar): 餐廳名
        - restaurant_address (varchar): 餐廳地址
    - User
        - member_id (varchar): 使用者id
        - member_password (varchar): 使用者密碼
        - member_email (varchar): 使用者email