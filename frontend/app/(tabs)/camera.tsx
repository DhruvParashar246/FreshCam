import React, { useRef, useState, useEffect } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import { useRouter } from "expo-router";

export default function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [isReady, setIsReady] = useState(false);
  const cameraRef = useRef<CameraView | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!permission) requestPermission();
  }, [permission]);

  if (!permission) return <View><Text>Loading permissions...</Text></View>;

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.permissionText}>
          We need camera access to scan your fruit 🍌
        </Text>
        <TouchableOpacity onPress={requestPermission} style={styles.grantBtn}>
          <Text style={styles.grantText}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.5,
        base64: false,
      });
      router.replace({
        pathname: "/result",
        params: { imageUri: photo.uri },
      });
    }
  };

  return (
    <View style={styles.container}>
      <CameraView
        style={styles.camera}
        ref={cameraRef}
        onCameraReady={() => setIsReady(true)}
      />
      <View style={styles.overlay}>
        <Text style={styles.overlayText}>Align your fruit inside the frame 🍎</Text>
      </View>
      <TouchableOpacity
        style={[styles.captureButton, { opacity: isReady ? 1 : 0.6 }]}
        onPress={takePicture}
        disabled={!isReady}
        activeOpacity={0.8}
      >
        <View style={styles.innerCircle} />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000" },
  camera: { flex: 1, width: "100%" },
  overlay: {
    position: "absolute",
    top: 60,
    alignSelf: "center",
    backgroundColor: "#00000070",
    padding: 10,
    borderRadius: 10,
  },
  overlayText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "500",
  },
  captureButton: {
    position: "absolute",
    bottom: 50,
    alignSelf: "center",
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: "#fff",
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 5,
  },
  innerCircle: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: "#4CAF50",
  },
  permissionText: {
    color: "#fff",
    textAlign: "center",
    marginBottom: 20,
    fontSize: 16,
  },
  grantBtn: {
    backgroundColor: "#4CAF50",
    paddingHorizontal: 25,
    paddingVertical: 10,
    borderRadius: 20,
  },
  grantText: { color: "#fff", fontWeight: "600", fontSize: 16 },
});
