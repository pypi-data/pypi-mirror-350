/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/


/// Returns mangled LLVM intrinsic function name matching the operation
/// variant.
std::string mlir::x86vector::OneToOneIntrinsicOp::getIntrinsicName() {
      return getImpl()->getIntrinsicName(getImpl(), getOperation());
  }

/// Returns operands for a corresponding LLVM intrinsic.
/// 
/// Additional operations may be created to facilitate mapping
/// between the source operands and the target intrinsic.
SmallVector<Value> mlir::x86vector::OneToOneIntrinsicOp::getIntrinsicOperands(::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter & typeConverter, ::mlir::RewriterBase & rewriter) {
      return getImpl()->getIntrinsicOperands(getImpl(), getOperation(), operands, typeConverter, rewriter);
  }
