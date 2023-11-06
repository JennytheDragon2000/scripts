#! /bin/bash
#
sudo apt-get update
sudo apt-get install update
sudo apt-get -y install default-jdk

sudo addgroup hadoop
sudo adduser --ingroup hadoop hadoopusr
sudo adduser hadoopusr sudo

sudo apt-get install openssh-server
su - hadoopusr

ssh-keygen -t rsa -P ""
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
ssh localhost

wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
sudo tar xvzf hadoop-3.3.6.tar.gz -C /usr/local/

echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> $HOME/.bashrc
echo "export HADOOP_HOME=/usr/local/hadoop" >> $HOME/.bashrc
echo "export PATH=$PATH:$HADOOP_HOME/bin" >> $HOME/.bashrc
echo "export PATH=$PATH:$HADOOP_HOME/sbin" >> $HOME/.bashrc
echo "export HADOOP_MAPRED_HOME=$HADOOP_HOME" >> $HOME/.bashrc
echo "export HADOOP_COMMON_HOME=$HADOOP_HOME" >> $HOME/.bashrc
echo "export HADOOP_HDFS_HOME=$HADOOP_HOME" >> $HOME/.bashrc
echo "export YARN_HOME=$HADOOP_HOME" >> $HOME/.bashrc
echo "export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native" >> $HOME/.bashrc
echo "export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib"" >> $HOME/.bashrc
source ~/.bashrc

echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

property="<property>\n\t<name>fs.default.name</name>\n\t<value>hdfs://localhost:9000</value>\n</property>"

sed -i.bak -e "/<\/configuration>/i $property" /usr/local/hadoop/etc/hadoop/core-site.xml

content="<property> 
<name>dfs.replication</name> 
<value>1</value> 
</property> 
<property> 
<name>dfs.namenode.name.dir</name> 
<value>file:/usr/local/hadoop_tmp/hdfs/namenode</value> 
</property> 
<property> 
<name>dfs.datanode.data.dir</name> 
<value>file:/usr/local/hadoop_tmp/hdfs/datanode</value> 
</property>"

sed -i.bak -e "/<\/configuration>/i $content" /usr/local/hadoop/etc/hadoop/hdfs-site.xml

content2="
<property> 
<name>yarn.nodemanager.aux-services</name> 
<value>mapreduce_shuffle</value> 
</property> 
<property> 
<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name> 
<value>org.apache.hadoop.mapred.ShuffleHandler</value> 
</property>
"

sed -i.bak -e "/<\/configuration>/i $content2" /usr/local/hadoop/etc/hadoop/yarn-site.xml

content3="
<property> 
<name>mapreduce.framework.name</name> 
<value>yarn</value> 
</property>
"

sed -i.bak -e "/<\/configuration>/i $content2" /usr/local/hadoop/etc/hadoop/mapred-site.xml


sudo mkdir -p /usr/local/hadoop_space
sudo mkdir -p /usr/local/hadoop_space/hdfs/namenode
sudo mkdir -p /usr/local/hadoop_space/hdfs/datanode

sudo chown -R hadoopusr /usr/local/hadoop_space

hdfs namenode -format
start-dfs.sh
start-yarn.sh
jps

