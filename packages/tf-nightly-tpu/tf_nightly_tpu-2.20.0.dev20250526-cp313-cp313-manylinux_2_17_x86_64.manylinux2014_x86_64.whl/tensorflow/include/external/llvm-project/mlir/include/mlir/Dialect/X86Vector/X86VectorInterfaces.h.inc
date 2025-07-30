/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace x86vector {
/// Interface for 1-to-1 conversion of an operation into LLVM intrinsics.
/// 
///     An op implementing this interface can be simply replaced by a call
///     to a matching intrinsic function.
///     The op must ensure that the combinations of their arguments and results
///     have valid intrinsic counterparts.
/// 
///     For example, an operation supporting different vector widths:
///     ```mlir
///       %res_v8 = x86vector.op %value_v8 : vector<8xf32>
///       %res_v16 = x86vector.op %value_v16 : vector<16xf32>
///     ```
///     can be converted to the following intrinsic calls:
///     ```mlir
///       %res_v8 = llvm.call_intrinsic "llvm.x86.op.intr.256"(%value_v8)
///       %res_v16 = llvm.call_intrinsic "llvm.x86.op.intr.512"(%value_v16)
///     ```
class OneToOneIntrinsicOp;
namespace detail {
struct OneToOneIntrinsicOpInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    std::string (*getIntrinsicName)(const Concept *impl, ::mlir::Operation *);
    SmallVector<Value> (*getIntrinsicOperands)(const Concept *impl, ::mlir::Operation *, ::mlir::ArrayRef<Value>, const ::mlir::LLVMTypeConverter &, ::mlir::RewriterBase &);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::x86vector::OneToOneIntrinsicOp;
    Model() : Concept{getIntrinsicName, getIntrinsicOperands} {}

    static inline std::string getIntrinsicName(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline SmallVector<Value> getIntrinsicOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter & typeConverter, ::mlir::RewriterBase & rewriter);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::x86vector::OneToOneIntrinsicOp;
    FallbackModel() : Concept{getIntrinsicName, getIntrinsicOperands} {}

    static inline std::string getIntrinsicName(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline SmallVector<Value> getIntrinsicOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter & typeConverter, ::mlir::RewriterBase & rewriter);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
    SmallVector<Value> getIntrinsicOperands(::mlir::Operation *tablegen_opaque_val, ::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter &typeConverter, ::mlir::RewriterBase &rewriter) const;
  };
};
template <typename ConcreteOp>
struct OneToOneIntrinsicOpTrait;

} // namespace detail
class OneToOneIntrinsicOp : public ::mlir::OpInterface<OneToOneIntrinsicOp, detail::OneToOneIntrinsicOpInterfaceTraits> {
public:
  using ::mlir::OpInterface<OneToOneIntrinsicOp, detail::OneToOneIntrinsicOpInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::OneToOneIntrinsicOpTrait<ConcreteOp> {};

  /// Returns mangled LLVM intrinsic function name matching the operation
  /// variant.
  std::string getIntrinsicName();

  /// Returns operands for a corresponding LLVM intrinsic.
  /// 
  /// Additional operations may be created to facilitate mapping
  /// between the source operands and the target intrinsic.
  SmallVector<Value> getIntrinsicOperands(::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter & typeConverter, ::mlir::RewriterBase & rewriter);
};
namespace detail {
  template <typename ConcreteOp>
  struct OneToOneIntrinsicOpTrait : public ::mlir::OpInterface<OneToOneIntrinsicOp, detail::OneToOneIntrinsicOpInterfaceTraits>::Trait<ConcreteOp> {

    /// Returns operands for a corresponding LLVM intrinsic.
    /// 
    /// Additional operations may be created to facilitate mapping
    /// between the source operands and the target intrinsic.
    SmallVector<Value> getIntrinsicOperands(::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter & typeConverter, ::mlir::RewriterBase & rewriter) {
      return SmallVector<Value>(operands);
    }
  };
}// namespace detail
} // namespace x86vector
} // namespace mlir
namespace mlir {
namespace x86vector {
template<typename ConcreteOp>
std::string detail::OneToOneIntrinsicOpInterfaceTraits::Model<ConcreteOp>::getIntrinsicName(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getIntrinsicName();
}
template<typename ConcreteOp>
SmallVector<Value> detail::OneToOneIntrinsicOpInterfaceTraits::Model<ConcreteOp>::getIntrinsicOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter & typeConverter, ::mlir::RewriterBase & rewriter) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getIntrinsicOperands(operands, typeConverter, rewriter);
}
template<typename ConcreteOp>
std::string detail::OneToOneIntrinsicOpInterfaceTraits::FallbackModel<ConcreteOp>::getIntrinsicName(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getIntrinsicName(tablegen_opaque_val);
}
template<typename ConcreteOp>
SmallVector<Value> detail::OneToOneIntrinsicOpInterfaceTraits::FallbackModel<ConcreteOp>::getIntrinsicOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter & typeConverter, ::mlir::RewriterBase & rewriter) {
  return static_cast<const ConcreteOp *>(impl)->getIntrinsicOperands(tablegen_opaque_val, operands, typeConverter, rewriter);
}
template<typename ConcreteModel, typename ConcreteOp>
SmallVector<Value> detail::OneToOneIntrinsicOpInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getIntrinsicOperands(::mlir::Operation *tablegen_opaque_val, ::mlir::ArrayRef<Value> operands, const ::mlir::LLVMTypeConverter &typeConverter, ::mlir::RewriterBase &rewriter) const {
return SmallVector<Value>(operands);
}
} // namespace x86vector
} // namespace mlir
