tee /opt/service/cloud.conf <<- 'EOF'
spring_cloud_nacos_config_serveraddr= 
spring_cloud_nacos_config_namespace=
#spring_cloud_nacos_config_username=ENC()
spring_cloud_nacos_config_password=ENC()
spring_cloud_nacos_discovery_serveraddr=
spring_cloud_nacos_discovery_namespace=
#spring_cloud_nacos_discovery_username=ENC()
spring_cloud_nacos_discovery_password=ENC()
spring_profiles_active=prod
EOF