// Prints "path x y w h; x y w h; ..." for every face (source px of the image, top-left origin).
import Vision
import AppKit
for p in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: p), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print(p); continue }
    let req = VNDetectFaceRectanglesRequest()
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let W = Double(cg.width), H = Double(cg.height)
    let s = (req.results ?? []).map { f -> String in
        let b = f.boundingBox
        return "\(Int(b.minX * W)) \(Int((1 - b.maxY) * H)) \(Int(b.width * W)) \(Int(b.height * H))"
    }.joined(separator: "; ")
    print(p, s)
}
