# İş Problemi

İş birimleri (X, Y, Z), belirli periyotlarda ürün bazlı sipariş durumlarını izlemek istemektedir.
Her bir iş birimi aşağıdaki sorulara hızlıca yanıt almak istemektedir:

“Sipariş XX içinde ürün YY teslim edildi mi?”

“Ödemesi alındı mı?”

“Sipariş ya da ürün iptal edildi mi?”

Bu ihtiyacı karşılamak için, orders.csv, order_items.csv ve products.csv dosyalarındaki veriler PostgreSQL’e yüklenmiş, ardından bu tablolardan birleşik bir görünüm (view) oluşturulmuştur. Bu view Airflow tarafından her saat başı otomatik olarak güncellenmektedir.

# Veri Yükleme

CSV dosyaları Docker Postgres konteynerine aktarılmış ve traindb.staging şemasına aşağıdaki tablolar olarak yüklenmiştir:

staging.orders

staging.order_items

staging.products

Bu veritabanı tabloları daha sonra view oluşturma işleminde kaynak olarak kullanılmıştır.

# Airflow DAG Tasarımı

Airflow üzerinde aşağıdaki adımları gerçekleştiren bir DAG geliştirilmiştir:

create_serving_schema

serving şemasını oluşturur (yoksa)

create_v_product_status_track

staging.orders, staging.order_items ve staging.products tablolarını kullanarak
serving.v_product_status_track view’ini CREATE OR REPLACE VIEW komutu ile oluşturur.

preview_v_product_status_track

Oluşturulan view’den örnek 20 satırı okur

Bu satırları Airflow task loguna yazar



# Oluşturulan View

Airflow DAG, aşağıdaki SQL ile business ihtiyacını karşılayan view’i oluşturur:

```
CREATE OR REPLACE VIEW serving.v_product_status_track AS
SELECT
    o.order_id,
    o.order_date,
    o.order_status,
    oi.order_item_id,
    oi.order_item_order_id,
    oi.order_item_product_id AS product_id,
    p.product_name,
    oi.order_item_quantity,
    oi.order_item_subtotal,
    oi.order_item_product_price,
    CASE WHEN o.order_status IN ('COMPLETE', 'CLOSED') THEN TRUE ELSE FALSE END AS is_delivered,
    CASE WHEN o.order_status NOT IN ('PENDING_PAYMENT','CANCELED','SUSPECTED_FRAUD') THEN TRUE ELSE FALSE END AS is_paid,
    CASE WHEN o.order_status = 'CANCELED' THEN TRUE ELSE FALSE END AS is_cancelled
FROM staging.orders o
JOIN staging.order_items oi ON o.order_id = oi.order_item_order_id
JOIN staging.products p ON oi.order_item_product_id = p.product_id;
```
![airflow1.png](/airflow1.png)
![output.png](/output.png)
![airflow2.png](/airflow2.png)
