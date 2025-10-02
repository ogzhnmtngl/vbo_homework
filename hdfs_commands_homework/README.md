# hdfs_commands_homework

.yaml dosyasının bulunduğu klasöre cd komutuyla girilir. Dosya yolunda dataops klasörü local olarak tanımlandığından, Hadoop cluster’a aktarılacak dosya önce bu klasöre indirilir ve ardından cluster’a yüklenir.

```bash
cd 00_big_data_playgrounds/dataops

wget https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv
```

## Docker Login & Docker Pull
.yaml dosyası içerisinde tanımlı imagelar DockerHub reposundan geldiği için öncelikle DockerHub’a login olmak gerekiyor. Sonrasında containerları ayağa kaldırmak için gerekli imagelar ilgili repodan çekilerek çalıştırılıyor.

```bash
docker login

docker pull veribilimiokulu/ubuntu_hadoop_hive_sqoop:3.0
```
![docker-login](images/docker-login.png)

## Docker-Compose 

`.yaml` dosyasının olduğu klasöre cd ile girdikten sonra containerları ayağa kaldırmak için docker compose komutunu uyguluyoruz.

```bash
docker compose up -d

```
![docker-compose](images/compose-up.png)

Kurulum tamamlandıktan sonra, aşağıdaki komut ile çalışan containerlar görüntülenebilir:

```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```

![docker-ps](images/docker-ps.png)

## Hadoop ortamına bağlanma

Master Node üzerinde işlem yapabilmek için ilgili container’a aşağıdaki komut ile bağlanılır:

```bash
docker exec -it cluster-master bash

```
Bu komut ile cluster-master container ına giriş yapılır. Ardından Hadoop komut satırı arayüzüne (CLI) erişim sağlanarak gerekli Hadoop komutları çalıştırılabilir.

### İşlem yapacağımız klasörleri oluşturma

Hadoop CLI’ye giriş yaptıktan sonra, HDFS içerisinde klasör oluşturmak için -mkdir komutu kullanılır. Örneğin, ödev klasörlerini oluşturmak için:

```bash

hdfs dfs -mkdir -p /user/root/hdfs_odev
hdfs dfs -mkdir -p /tmp/hdfs_odev

```
![folders](images/hdfs-mkdir-folder.png)

### Masternode ui üzerinde görüntüleme 

Master Node UI üzerinden HDFS’de oluşturduğumuz dosyaları görüntüleyebilmek için, VM üzerinde çalışan containerlara dışarıdan erişim sağlanması gerekir.

Bu erişimi sağlamak için port-forwarding işlemi uygulanır. VM ortamı kullanıldığından, ilgili portlar host makineye yönlendirilerek web arayüzüne erişim mümkün hale gelir.

![forwarding](images/forwarding.png)

![masternodeui](images/ui1.png)


### Wine.csv dosyasını localden hadoop'a aktarma

Local ortamdan Hadoop HDFS’e Wine.csv dosyasını aktarmak için aşağıdaki komutlar kullanılabilir:

```bash

 hdfs dfs -put Wine.csv /user/root/hdfs_odev

```

![put](images/put.png)

![masternodeui](images/ui2.png)

### Wine.csv dosyasını tmp/hdfs_odev klasörüne kopyalama

HDFS üzerinde bir dosyayı veya klasörü başka bir dizine kopyalamak için -cp komutu kullanılır. 

```bash

 hdfs dfs -put Wine.csv /user/root/hdfs_odev

```
![cp](images/-cp.png)

![copy](images/ui3.png)


### HDFS üzerinden dosyayı silme 

Hadoop HDFS’de bir dosyayı (Trash) gitmeden tamamen silmek için -skipTrash parametresi kullanılır.

```bash

hdfs dfs -rm -r -skipTrash /tmp/hdfs_odev

```

![-rm](images/rm.png)

![rm-ui](images/ui4.png)


