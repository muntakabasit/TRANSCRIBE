//
//  TranscriptCard.swift
//  DAWT-Transcribe
//
//  Card displaying a single transcript segment with timestamp
//

import SwiftUI

struct TranscriptCard: View {
    let segment: Segment

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            DAWTDesign.Typography.timestamp(segment.timestamp)

            DAWTDesign.Typography.body(segment.text)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .dawtCard()
    }
}

#Preview {
    VStack(spacing: 16) {
        TranscriptCard(segment: Segment(
            timestamp: "0:00 - 0:10",
            startTime: "0:00",
            endTime: "0:10",
            text: "I love you. I care about you. I'm thinking of you right now."
        ))

        TranscriptCard(segment: Segment(
            timestamp: "0:11 - 0:17",
            startTime: "0:11",
            endTime: "0:17",
            text: "I'm here for you, always."
        ))
    }
    .padding()
    .background(DAWTDesign.Colors.background)
}
