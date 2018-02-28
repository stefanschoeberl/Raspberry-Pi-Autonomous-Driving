//
//  ViewController.swift
//  UDPClient
//
//  Created by Stefan Schöberl on 30.12.17.
//  Copyright © 2017 Stefan Schöberl. All rights reserved.
//

import UIKit
import CoreMotion

import CocoaAsyncSocket

class ViewController: UIViewController {
    
    let socket = GCDAsyncUdpSocket()
    let mm = CMMotionManager()
    let notificationFeedbackGenerator = UINotificationFeedbackGenerator()
    let selectionFeedbackGenerator = UISelectionFeedbackGenerator()
    
    var direction: UInt8 = 0 {
        didSet {
            if direction != oldValue {
                selectionFeedbackGenerator.selectionChanged()
            }
        }
    }
    
    var backwardsPressed = false
    var forwardPressed = false
    
    var firstUpdate = true
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let interval = 0.01
        
        mm.deviceMotionUpdateInterval = interval
        mm.startDeviceMotionUpdates(to: OperationQueue.main) { [unowned self] (_, _) in
            self.transmit()
        }
        
    }

    @IBAction func beginBackwards(_ sender: Any) {
        backwardsPressed = true
        direction = 2
    }
    
    @IBAction func stopBackwards(_ sender: Any) {
        backwardsPressed = false
        direction = forwardPressed ? 1 : 0
    }
    
    @IBAction func beginForward(_ sender: Any) {
        forwardPressed = true
        direction = 1
    }
    
    @IBAction func stopForward(_ sender: Any) {
        forwardPressed = false
        direction = backwardsPressed ? 2 : 0
    }
    
    func transmit() {
        guard let gravity = mm.deviceMotion?.gravity else {
            return
        }
        
        var angle = max(min(gravity.y * 2, 1), -1)
        let angleData = NSData(bytes: &angle, length: MemoryLayout.size(ofValue: angle)) as Data
        
        let directionData = NSData(bytes: &direction, length: MemoryLayout.size(ofValue: direction)) as Data
        
        var data = Data()
        data.append(directionData)
        data.append(angleData)
        
        socket.send(data, toHost: "10.20.30.40", port: 5555, withTimeout: -1, tag: -1)
        
        if (self.firstUpdate) {
            self.firstUpdate = false
            self.notificationFeedbackGenerator.notificationOccurred(.success)
        }
    }    
}
