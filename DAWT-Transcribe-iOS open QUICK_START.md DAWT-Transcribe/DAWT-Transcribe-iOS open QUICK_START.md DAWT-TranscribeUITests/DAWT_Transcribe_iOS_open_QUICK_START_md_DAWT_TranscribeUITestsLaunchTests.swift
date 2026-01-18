//
//  DAWT_Transcribe_iOS_open_QUICK_START_md_DAWT_TranscribeUITestsLaunchTests.swift
//  DAWT-Transcribe-iOS open QUICK_START.md DAWT-TranscribeUITests
//
//  Created by Abdul Basit Muntaka on 16/01/2026.
//

import XCTest

final class DAWT_Transcribe_iOS_open_QUICK_START_md_DAWT_TranscribeUITestsLaunchTests: XCTestCase {

    override class var runsForEachTargetApplicationUIConfiguration: Bool {
        true
    }

    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    @MainActor
    func testLaunch() throws {
        let app = XCUIApplication()
        app.launch()

        // Insert steps here to perform after app launch but before taking a screenshot,
        // such as logging into a test account or navigating somewhere in the app

        let attachment = XCTAttachment(screenshot: app.screenshot())
        attachment.name = "Launch Screen"
        attachment.lifetime = .keepAlways
        add(attachment)
    }
}
