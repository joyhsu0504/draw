//
//  ViewController.swift
//  Picasso
//
//  Created by Gokul Swamy on 11/11/16.
//  Copyright © 2016 Gokul Swamy. All rights reserved.
//

import UIKit
import Speech
import AVFoundation
import AudioToolbox

class ViewController: UIViewController, SFSpeechRecognizerDelegate, AVCapturePhotoCaptureDelegate, AVSpeechSynthesizerDelegate, AVAudioPlayerDelegate{
    
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale.init(identifier: "en-US"))
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    var imageOutput : AVCaptureStillImageOutput?
    var session: AVCaptureSession?
    @IBOutlet var recordButton: NSLayoutConstraint!
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        speechRecognizer?.delegate = self
        SFSpeechRecognizer.requestAuthorization { (SFSpeechRecognizerAuthorizationStatus) in
            print("authorization requested")
        }
        let captureDevice : AVCaptureDevice? = initCaptureDevice()
        initOutput()
        if (captureDevice != nil) {
            let deviceInput : AVCaptureInput? = initInputDevice(captureDevice: captureDevice!)
            if (deviceInput != nil) {
                initSession(deviceInput: deviceInput!)
                let previewLayer: AVCaptureVideoPreviewLayer = AVCaptureVideoPreviewLayer(session: self.session)
                previewLayer.frame = self.view.bounds
                self.view.layer.addSublayer(previewLayer)
                self.session?.startRunning()
            }
        }
        else {
            print("Missing Camera")
        }
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    
    @IBAction func startListening(_ sender: AnyObject) {
        if recognitionTask != nil {
            recognitionTask?.cancel()
            recognitionTask = nil
        }
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(AVAudioSessionCategoryRecord)
            try audioSession.setMode(AVAudioSessionModeMeasurement)
            try audioSession.setActive(true, with: .notifyOthersOnDeactivation)
        }
        catch {
            print("audioSession properties weren't set because of an error.")
        }
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let inputNode = audioEngine.inputNode else {
            fatalError("Audio engine has no input node")
        }
        guard let recognitionRequest = recognitionRequest else {
            fatalError("Unable to create an SFSpeechAudioBufferRecognitionRequest object")
        }
        recognitionRequest.shouldReportPartialResults = true
        recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest, resultHandler: { (result, error) in
            var isFinal = false
            var backCameraDevice: AVCaptureDevice
            if result != nil {
                var text = result?.bestTranscription.formattedString.lowercased()
                if text?.range(of: "take a pic") != nil{
                    print("detected")
                    text = ""
                    self.audioEngine.stop()
                    self.recognitionRequest?.endAudio()
                    self.toggleFlash()
                    self.toggleFlash()
                    self.toggleFlash()
                    self.toggleFlash()
                    self.toggleFlash()
                    self.toggleFlash()
                    self.shutter()
                    self.takePhoto()
                    UIApplication.shared.open(NSURL(string:"ifttt://") as! URL, options: [:], completionHandler: nil)
                }
                isFinal = (result?.isFinal)!
            }
            if error != nil || isFinal {
                self.audioEngine.stop()
                inputNode.removeTap(onBus: 0)
                self.recognitionRequest = nil
                self.recognitionTask = nil
            }
        })
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { (buffer, when) in
            self.recognitionRequest?.append(buffer)
        }
        audioEngine.prepare()
        do {
            try audioEngine.start()
        } catch {
            print("audioEngine couldn't start because of an error.")
        }
    }
    
    private func initCaptureDevice() -> AVCaptureDevice? {
        var captureDevice: AVCaptureDevice?
        let devices: NSArray = AVCaptureDevice.devices() as NSArray
        for device in devices {
            if (device as AnyObject).position == AVCaptureDevicePosition.back {
                captureDevice = device as? AVCaptureDevice
            }
        }
        return captureDevice
    }
    
    private func initInputDevice(captureDevice : AVCaptureDevice) -> AVCaptureInput? {
        var deviceInput : AVCaptureInput?
        do {
            deviceInput = try AVCaptureDeviceInput(device: captureDevice)
        }
        catch _ {
            deviceInput = nil
        }
        return deviceInput
    }
    
    private func initOutput() {
        self.imageOutput = AVCaptureStillImageOutput()
    }
    
    private func initSession(deviceInput: AVCaptureInput) {
        self.session = AVCaptureSession()
        self.session?.sessionPreset = AVCaptureSessionPresetPhoto
        self.session?.addInput(deviceInput)
        self.session?.addOutput(self.imageOutput!)
    }
    
    private func takePhoto() {
        let videoConnection : AVCaptureConnection? = self.imageOutput?.connection(withMediaType: AVMediaTypeVideo)
        if (videoConnection != nil) {
            self.imageOutput?.captureStillImageAsynchronously(from: videoConnection, completionHandler: { (imageDataSampleBuffer, error) -> Void in
                if (imageDataSampleBuffer != nil) {
                    let imageData : NSData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(imageDataSampleBuffer) as NSData
                    let image = UIImage(data: imageData as Data)
                    UIImageWriteToSavedPhotosAlbum(image!, nil, nil, nil)
                    //IFTTT Uploads after save.
                }
            })
        }
    }
    

    func shutter(){
        AudioServicesPlayAlertSound(SystemSoundID(1108))
    }
    
    func toggleFlash() {
        let device = AVCaptureDevice.defaultDevice(withMediaType: AVMediaTypeVideo)
        if (device?.hasTorch)! {
            do {
                try device?.lockForConfiguration()
                if (device?.torchMode == AVCaptureTorchMode.on) {
                    device?.torchMode = AVCaptureTorchMode.off
                } else {
                    do {
                        try device?.setTorchModeOnWithLevel(1.0)
                    } catch {
                        print(error)
                    }
                }
                device?.unlockForConfiguration()
            } catch {
                print(error)
            }
        }
        sleep(1)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    


}

