
## Exercise Starter Code
The current folder conatins the following starter code for the classroom exercises:
```bash
.
├── Vagrantfile        # Vagrant exercise
├── go-helloworld      # Docker and Kubernetes exercise
│   ├── README.md
│   └── main.go
├── manifests
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── namespace.yaml
│   └── service.yaml
└── python-helloworld  # Docker walkthrough code  
    ├── app.py
    └── requirements.txt
```


**Note**: the specified `config.vm.box_version` in the Vagrantfile updates with time. You will have to change it from `212` shown in the demo video above to a newer version. When a particular version used in Vagrantfile becomes deprecated, the command prompt will show you all available newer versions.

**Note on VirtualBox 7.1 + Vagrant compatibility**: The Vagrantfile works on both Vagrant 2.2.10+/VirtualBox 6.1.x and Vagrant 2.4.x/VirtualBox 7.1.x. However, official Vagrant support for VirtualBox 7.1 was added in **Vagrant 2.4.2**. If you are running Vagrant 2.4.0 or 2.4.1 against VirtualBox 7.1, `vagrant up` will print a warning that the installed VirtualBox version is not officially supported by the provider. The VM will usually still come up, but to avoid the warning (and any subtle provider issues) upgrade to Vagrant 2.4.2 or later. 


