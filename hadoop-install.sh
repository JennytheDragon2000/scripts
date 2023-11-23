#! /bin/bash
#
sudo apt-get update
sudo apt-get install update
sudo apt-get -y install default-jdk

sudo addgroup hadoop
sudo adduser --ingroup hadoop hadoopusr
sudo adduser hadoopusr sudo

sudo apt-get install openssh-server

sudo -u hadoopusr -H ssh-keygen -t rsa -P ""
sudo -u hadoopusr -H cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys

sudo -u hadoopusr -H ssh localhost

sudo -u hadoopusr -H wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
sudo -u hadoopusr -H tar xvzf hadoop-3.3.6.tar.gz 
sudo -u hadoopusr -H sudo mv hadoop-3.3.6 hadoop
sudo -u hadoopusr -H mv hadoop /usr/local/hadoop

sudo -u hadoopusr -H echo "export java_home=/usr/lib/jvm/java-11-openjdk-amd64" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export hadoop_home=/usr/local/hadoop" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export path=\$path:\$hadoop_home/bin" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export path=\$path:\$hadoop_home/sbin" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export hadoop_mapred_home=\$hadoop_home" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export hadoop_common_home=\$hadoop_home" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export hadoop_hdfs_home=\$hadoop_home" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export yarn_home=\$hadoop_home" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export hadoop_common_lib_native_dir=\$hadoop_home/lib/native" >> $HOME/.bashrc
sudo -u hadoopusr -H echo "export hadoop_opts='-djava.library.path=$hadoop_home/lib/native'"


sudo -u hadoopusr -H source ~/.bashrc


sudo -u hadoopusr -H echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh


sudo -u hadoopusr -H property="<property>\n\t<name>fs.default.name</name>\n\t<value>hdfs://localhost:9000</value>\n</property>"
sudo -u hadoopusr -H sed -i.bak -e "/<\/configuration>/i $property" /usr/local/hadoop/etc/hadoop/core-site.xml

sudo -u hadoopusr -H content="<property>\n\t<name>dfs.replication</name>\n\t<value>1</value>\n</property>\n<property>\n\t<name>dfs.namenode.name.dir</name>\n\t<value>file:/usr/local/hadoop_tmp/hdfs/namenode</value>\n</property>\n<property>\n\t<name>dfs.datanode.data.dir</name>\n\t<value>file:/usr/local/hadoop_tmp/hdfs/datanode</value>\n</property>"
sudo -u hadoopusr -H sed -i.bak -e "/<\/configuration>/i $content" /usr/local/hadoop/etc/hadoop/hdfs-site.xml

sudo -u hadoopusr -H content2="<property>\n\t<name>yarn.nodemanager.aux-services</name>\n\t<value>mapreduce_shuffle</value>\n</property>\n<property>\n\t<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>\n\t<value>org.apache.hadoop.mapred.ShuffleHandler</value>\n</property>"
sudo -u hadoopusr -H sed -i.bak -e "/<\/configuration>/i $content2" /usr/local/hadoop/etc/hadoop/yarn-site.xml

content3="<property>\n\t<name>mapreduce.framework.name</name>\n\t<value>yarn</value>\n</property>"
sudo -u hadoopusr -H sed -i.bak -e "/<\/configuration>/i $content3" /usr/local/hadoop/etc/hadoop/mapred-site.xml


sudo -u hadoopusr -H sudo mkdir -p /usr/local/hadoop_space
sudo -u hadoopusr -H sudo mkdir -p /usr/local/hadoop_space/hdfs/namenode
sudo -u hadoopusr -H sudo mkdir -p /usr/local/hadoop_space/hdfs/datanode
sudo -u hadoopusr -H sudo chown -R hadoopusr /usr/local/hadoop_space

sudo -u hadoopusr -H sudo mkdir -p /usr/local/hadoop_tmp/hdfs/namenode
sudo -u hadoopusr -H sudo mkdir -p /usr/local/hadoop_tmp/hdfs/datanode
sudo -u hadoopusr -H sudo chown -R hadoopusr /usr/local/hadoop_tmp

sudo -u hadoopusr -H hdfs namenode -format
sudo -u hadoopusr -H start-dfs.sh
sudo -u hadoopusr -H start-yarn.sh
sudo -u hadoopusr -H jps

# ssh -v -L 9870:localhost:9870 -L 8088:localhost:8088 hadoopusr@139.162.41.103
