import CoreGraphics
import Foundation
import ImageIO
import Vision

func fail(_ message: String) -> Never {
    FileHandle.standardError.write((message + "\n").data(using: .utf8)!)
    exit(1)
}

guard CommandLine.arguments.count >= 2 else {
    fail("usage: macos_vision_ocr.swift IMAGE_PATH")
}

let imagePath = CommandLine.arguments[1]
let imageURL = URL(fileURLWithPath: imagePath)

guard let imageSource = CGImageSourceCreateWithURL(imageURL as CFURL, nil),
      let image = CGImageSourceCreateImageAtIndex(imageSource, 0, nil) else {
    fail("could not read image: \(imagePath)")
}

let width = image.width
let height = image.height

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
request.recognitionLanguages = ["en-US"]

let handler = VNImageRequestHandler(cgImage: image, options: [:])
do {
    try handler.perform([request])
} catch {
    fail("vision OCR failed: \(error)")
}

func cleanTSV(_ text: String) -> String {
    return text
        .replacingOccurrences(of: "\t", with: " ")
        .replacingOccurrences(of: "\n", with: " ")
        .replacingOccurrences(of: "\r", with: " ")
}

print("level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext")
print("1\t1\t0\t0\t0\t0\t0\t0\t\(width)\t\(height)\t-1\t")

let observations = (request.results ?? []).sorted {
    let lhs = $0.boundingBox
    let rhs = $1.boundingBox
    let lhsTop = 1.0 - lhs.origin.y - lhs.height
    let rhsTop = 1.0 - rhs.origin.y - rhs.height
    if abs(lhsTop - rhsTop) > 0.01 {
        return lhsTop < rhsTop
    }
    return lhs.origin.x < rhs.origin.x
}

for (index, observation) in observations.enumerated() {
    guard let candidate = observation.topCandidates(1).first else {
        continue
    }

    let box = observation.boundingBox
    let left = Int((box.origin.x * Double(width)).rounded())
    let top = Int(((1.0 - box.origin.y - box.height) * Double(height)).rounded())
    let boxWidth = Int((box.width * Double(width)).rounded())
    let boxHeight = Int((box.height * Double(height)).rounded())
    let conf = Int((candidate.confidence * 100.0).rounded())
    let text = cleanTSV(candidate.string)

    print("5\t1\t1\t1\t\(index + 1)\t1\t\(left)\t\(top)\t\(boxWidth)\t\(boxHeight)\t\(conf)\t\(text)")
}
