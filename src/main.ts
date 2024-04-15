import './style.css'
import { connect } from './scripts/client';

const retrieveVirtualCam = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const camera = devices.filter(device => device.kind === 'videoinput' && device.label === 'OBS Virtual Camera');
  
    if (camera.length === 0) {
      console.error('No OBS camera found');
      handleCamera(devices[0].deviceId)
    }

    handleCamera(camera[0].deviceId)
  } catch (error) {
    console.error(error)
  }
}

async function handleCamera(id: string) {
  const element: HTMLVideoElement | null = document.querySelector('.cam')
  const deviceId = id

  if(element !== null) {
    element.srcObject = null; // Clear previous stream (if any)
  }

  try {
    const constraints = { video: { deviceId } };
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    if(element !== null) {
      element.srcObject = stream;
    }
  } catch (error) {
    console.error('Error accessing camera:', error);
  }
}

window.onload = async () => {
  await retrieveVirtualCam()
  await connect()
}