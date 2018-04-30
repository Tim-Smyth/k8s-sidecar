from kubernetes import client, config, watch
import os
import sys


def writeTextToFile(folder, filename, data):
    with open(folder +"/"+ filename, 'w') as f:
        f.write(data)
        f.close()


def removeFile(folder, filename):
    completeFile = folder +"/"+filename
    if os.path.isfile(completeFile):
        os.remove(completeFile)
    else:
        sys.stderr.write("Error: %s file not found" % completeFile)


def watchForChanges(label, targetFolder):
    v1 = client.CoreV1Api()
    w = watch.Watch()
    for event in w.stream(v1.list_config_map_for_all_namespaces):
        if event['object'].metadata.labels is None:
            continue
        sys.stdout.write("Working on configmap %s" % event['object'].metadata.name)
        if label in event['object'].metadata.labels.keys():
            sys.stdout.write("Configmap with label found")
            dataMap=event['object'].data
            if dataMap is None:
                sys.stdout.write("Configmap does not have data.")
                continue
            eventType = event['type']
            for filename in dataMap.keys():
                sys.stdout.write("File in configmap %s %s" % (filename, eventType))
                if (eventType == "ADDED") or (eventType == "MODIFIED"):
                    writeTextToFile(targetFolder, filename, dataMap[filename])
                else:
                    removeFile(targetFolder, filename)


def main():
    sys.stdout.write("Starting config map collector")
    label = os.getenv('LABEL')
    if label is None:
        sys.stderr.write("Should have added LABEL as environment variable! Exit")
        return -1
    targetFolder = os.getenv('FOLDER')
    if targetFolder is None:
        sys.stderr.write("Should have added FOLDER as environment variable! Exit")
        return -1
    config.load_incluster_config()
    sys.stdout.write("Config for cluster api loaded...")
    watchForChanges(label, targetFolder)


if __name__ == '__main__':
    main()
