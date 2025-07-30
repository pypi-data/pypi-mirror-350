from collections.abc import Callable, Iterable, Iterator
import enum
import os
from typing import Annotated, overload

from numpy.typing import ArrayLike


def isVulkanAvailable() -> bool:
    """Returns True if Vulkan is available on this system."""

class Device:
    """
    Handle for a physical device implementing the Vulkan API. Contains basic properties of the device.
    """

    @property
    def name(self) -> str:
        """Name of the device"""

    @property
    def isDiscrete(self) -> bool:
        """
        True, if the device is a discrete GPU. Can be useful to distinguish from integrated ones.
        """

    def __repr__(self) -> str: ...

def enumerateDevices() -> list[Device]:
    """Returns a list of all supported installed devices."""

def getCurrentDevice() -> Device:
    """
    Returns the currently active device. Note that this may initialize the context.
    """

def selectDevice(id: int, force: bool = False) -> None:
    """
    Sets the device on which the context will be initialized. Set force=True if an existing context should be destroyed.
    """

def isDeviceSuitable(arg: int, /) -> bool:
    """
    Returns True if the device given by its id supports all enabled extensions
    """

def suitableDeviceAvailable() -> bool:
    """
    Returns True, if there is a device available supporting all enabled extensions
    """

def destroyResources() -> None:
    """Destroys all resources on the GPU and frees their allocated memory"""

def getResourceCount() -> int:
    """Counts the number of resources currently alive"""

class Resource:
    """Base class of all resources allocated on the GPU"""

    @property
    def destroyed(self) -> bool:
        """True, if the underlying resources have been destroyed."""

    def destroy(self) -> None:
        """Frees the allocated resources."""

    def __bool__(self) -> bool: ...

class ResourceSnapshot:
    """
    Takes a snapshot of currently alive resources and allows to destroy resources created afterwards.
    """

    def __init__(self) -> None: ...

    @property
    def count(self) -> int:
        """Number of resources created while context was activated"""

    def capture(self) -> None:
        """Takes a snapshot of currently alive resources"""

    def restore(self) -> None:
        """Destroys resources created since the last capture"""

    def __enter__(self) -> ResourceSnapshot: ...

    def __exit__(self, exc_type: object | None, exc_value: object | None, traceback: object | None) -> None: ...

class Command:
    """
    Base class for commands running on the device. Execution happens asynchronous after being submitted.
    """

class Subroutine(Resource):
    """
    Subroutines are reusable sequences of commands that can be submitted multiple times to the device. Recording sequence of commands require non negligible CPU time and may be amortized by reusing sequences via Subroutines.
    """

    @property
    def simultaneousUse(self) -> bool:
        """True, if the subroutine can be used simultaneous"""

def createSubroutine(commands: list, simultaneous: bool = False) -> Subroutine:
    """
    creates a subroutine from the list of commands

    Parameters
    ----------
    commands: Command[]
        Sequence of commands the Subroutine consists of
    simultaneous: bool, default=False
        True, if the subroutine can be submitted while a previous submission
        has not yet finished. Disobeying this requirement results in undefined
        behavior.
    """

class Timeline(Resource):
    """
    Timeline managing the execution of code and commands using an increasing internal counter. Both GPU and CPU can wait and/or increase this counter thus creating a synchronization between them or among themselves. The current value of the counter can be queried allowing an asynchronous method of reporting the progress.

    Parameters
    ----------
    value: int, default=0
        Initial value of the internal counter
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, initialValue: int) -> None: ...

    @property
    def id(self) -> int:
        """Id of this timeline"""

    @property
    def value(self) -> int:
        """
        Returns or sets the current value of the timeline. Note that the value can only increase. Disobeying this requirement results in undefined behavior.
        """

    @value.setter
    def value(self, arg: int, /) -> None: ...

    def wait(self, value: int) -> None:
        """Waits for the timeline to reach the given value."""

    def waitTimeout(self, value: int, timeout: int) -> bool:
        """
        Waits for the timeline to reach the given value for a certain amount. Returns True if the value was reached and False if it timed out.

        Parameters
        ----------
        value: int
            Value to wait for
        timeout: int
            Time in nanoseconds to wait. May be rounded to the closest internal precision of the device clock.
        """

    def __repr__(self) -> str: ...

class Submission:
    """
    Submissions are issued after work has been submitted to the device and can be used to wait for its completion.
    """

    @property
    def timeline(self) -> Timeline:
        """The timeline this submission was issued with."""

    @property
    def finalStep(self) -> int:
        """The value the timeline will reach when the submission finishes."""

    @property
    def forgettable(self) -> bool:
        """True, if the Submission can be discarded safely, i.e. fire and forget."""

    def wait(self) -> None:
        """Blocks the caller until the submission finishes."""

    def waitTimeout(self, ns: int) -> bool:
        """
        Blocks the caller until the submission finished or the specified time elapsed. Returns True in the first, False in the second case.
        """

class SequenceBuilder:
    """
    Builder class for recording a sequence of commands and subroutines and submitting it to the device for execution, which happens asynchronous, i.e. submit() returns before the recorded work finishes.
    """

    @overload
    def __init__(self, timeline: Timeline) -> None:
        """
        Creates a new SequenceBuilder.

        Parameters
        ----------
        timeline: Timeline
            Timeline to use for orchestrating commands and subroutines
        """

    @overload
    def __init__(self, timeline: Timeline, startValue: int) -> None:
        """
        Creates a new SequenceBuilder.

        Parameters
        ----------
        timeline: Timeline
            Timeline to use for orchestrating commands and subroutines
        startValue: int
            Counter value to wait for on the timeline to start with
        """

    @overload
    def And(self, cmd: Command) -> SequenceBuilder:
        """Issues the command to run parallel in the current step."""

    @overload
    def And(self, subroutine: Subroutine) -> SequenceBuilder:
        """Issues the subroutine to run parallel in the current step."""

    def AndList(self, list: list) -> SequenceBuilder:
        """Issues each element of the list to run parallel in the current step"""

    @overload
    def Then(self, cmd: Command) -> SequenceBuilder:
        """
        Issues a new step to execute after waiting for the previous one to finish.
        """

    @overload
    def Then(self, subroutine: Subroutine) -> SequenceBuilder: ...

    def NextStep(self) -> SequenceBuilder:
        """
        Issues a new step. Following calls to And are ensured to run after previous ones finished.
        """

    @overload
    def WaitFor(self, value: int) -> SequenceBuilder:
        """
        Issues the following steps to wait on the sequence timeline to reach the given value.
        """

    @overload
    def WaitFor(self, timeline: Timeline, value: int) -> SequenceBuilder:
        """
        Issues the following steps to wait for the given timeline to reach the given value
        """

    def printWaitGraph(self) -> str:
        """
        Returns a visualization of the current wait graph in the form: (Timeline.ID(WaitValue))* -> (submissions) -> (Timeline.ID(SignalValue)). Must be called before Submit().
        """

    def Submit(self) -> Submission:
        """Submits the recorded steps as a single batch to the GPU."""

@overload
def beginSequence(timeline: Timeline, startValue: int = 0) -> SequenceBuilder:
    """Starts a new sequence."""

@overload
def beginSequence() -> SequenceBuilder: ...

@overload
def execute(cmd: Command) -> None:
    """Runs the given command synchronous."""

@overload
def execute(sub: Subroutine) -> None:
    """Runs the given subroutine synchronous."""

def executeList(list: list) -> None:
    """Runs the given of list commands synchronous"""

class HeaderMap:
    """
    Dict mapping filepaths to shader source code. Consumed by Compiler to resolve include directives.
    """

    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: HeaderMap) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: dict[str, str], /) -> None:
        """Construct from a dictionary"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the map is nonempty"""

    def __repr__(self) -> str: ...

    @overload
    def __contains__(self, arg: str, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def __iter__(self) -> Iterator[str]: ...

    def __getitem__(self, arg: str, /) -> str: ...

    def __delitem__(self, arg: str, /) -> None: ...

    def clear(self) -> None:
        """Remove all items"""

    def __setitem__(self, arg0: str, arg1: str, /) -> None: ...

    def update(self, arg: HeaderMap, /) -> None:
        """Update the map with element from `arg`"""

    def __eq__(self, arg: object, /) -> bool: ...

    def __ne__(self, arg: object, /) -> bool: ...

    class ItemView:
        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[tuple[str, str]]: ...

    class KeyView:
        @overload
        def __contains__(self, arg: str, /) -> bool: ...

        @overload
        def __contains__(self, arg: object, /) -> bool: ...

        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[str]: ...

    class ValueView:
        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[str]: ...

    def keys(self) -> HeaderMap.KeyView:
        """Returns an iterable view of the map's keys."""

    def values(self) -> HeaderMap.ValueView:
        """Returns an iterable view of the map's values."""

    def items(self) -> HeaderMap.ItemView:
        """Returns an iterable view of the map's items."""

class Compiler:
    """
    Compiler for generating SPIR-V byte code used by Programs from shader code written in GLSL. Has additional methods to handle includes.
    """

    def __init__(self) -> None: ...

    def addIncludeDir(self, path: str | os.PathLike) -> None:
        """
        Adds a path to the list of include directories that take part in resolving includes.
        """

    def popIncludeDir(self) -> None:
        """Removes the last added include dir from the internal list"""

    def clearIncludeDir(self) -> None:
        """Clears the internal list of include directories"""

    @overload
    def compile(self, code: str) -> bytes:
        """Compiles the given GLSL code and returns the SPIR-V code as bytes"""

    @overload
    def compile(self, code: str, headers: HeaderMap) -> bytes:
        """
        Compiles the given GLSL code using the provided header files and returns the SPIR-V code as bytes
        """

class SubgroupProperties:
    """List of subgroup properties and supported operations"""

    @property
    def subgroupSize(self) -> int:
        """Threads per subgroup"""

    @property
    def basicSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_basic"""

    @property
    def voteSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_vote"""

    @property
    def arithmeticSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_arithmetic"""

    @property
    def ballotSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_ballot"""

    @property
    def shuffleSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_shuffle"""

    @property
    def shuffleRelativeSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_shuffle_relative"""

    @property
    def shuffleClusteredSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_clustered"""

    @property
    def quadSupport(self) -> bool:
        """Support for GL_KHR_shader_subgroup_quad"""

    @property
    def uniformControlFlowSupport(self) -> bool:
        """Support for GL_EXT_subgroup_uniform_control_flow"""

    @property
    def maximalReconvergenceSupport(self) -> bool:
        """Support for GL_EXT_maximal_reconvergence"""

    def __repr__(self) -> str: ...

@overload
def getSubgroupProperties() -> SubgroupProperties:
    """Returns the properties specific to subgroups (waves)."""

@overload
def getSubgroupProperties(arg: int, /) -> SubgroupProperties: ...

class ParameterType(enum.Enum):
    """Type of parameter"""

    COMBINED_IMAGE_SAMPLER = 1

    STORAGE_IMAGE = 3

    UNIFORM_BUFFER = 6

    STORAGE_BUFFER = 7

    ACCELERATION_STRUCTURE = 1000150000

class ImageBindingTraits:
    """Properties a binding expects from a bound image"""

    @property
    def format(self) -> ImageFormat:
        """Expected image format"""

    @property
    def dims(self) -> int:
        """Image dimensions"""

class BindingTraits:
    """Properties of binding found in programs"""

    @property
    def name(self) -> str:
        """Name of the binding. Might be empty."""

    @property
    def binding(self) -> int:
        """Index of the binding"""

    @property
    def type(self) -> ParameterType:
        """Type of the binding"""

    @property
    def imageTraits(self) -> ImageBindingTraits | None:
        """Properties of the image if one is expected"""

    @property
    def count(self) -> int:
        """Number of elements in binding, i.e. array size"""

    def __repr__(self) -> str: ...

class LocalSize:
    """
    Description if the local size, i.e. the number and arrangement of threads in a single thread group
    """

    def __init__(self) -> None: ...

    @property
    def x(self) -> int:
        """Number of threads in X dimension"""

    @x.setter
    def x(self, arg: int, /) -> None: ...

    @property
    def y(self) -> int:
        """Number of threads in Y dimension"""

    @y.setter
    def y(self, arg: int, /) -> None: ...

    @property
    def z(self) -> int:
        """Number of threads in Z dimension"""

    @z.setter
    def z(self, arg: int, /) -> None: ...

    def __repr__(self) -> str: ...

class DispatchCommand(Command):
    """Command for executing a program using the given group size"""

    @property
    def groupCountX(self) -> int:
        """Amount of groups in X dimension"""

    @groupCountX.setter
    def groupCountX(self, arg: int, /) -> None: ...

    @property
    def groupCountY(self) -> int:
        """Amount of groups in Y dimension"""

    @groupCountY.setter
    def groupCountY(self, arg: int, /) -> None: ...

    @property
    def groupCountZ(self) -> int:
        """Amount of groups in Z dimension"""

    @groupCountZ.setter
    def groupCountZ(self, arg: int, /) -> None: ...

class DispatchIndirectCommand(Command):
    """
    Command for executing a program using the group size read from the provided tensor at given offset
    """

    @property
    def tensor(self) -> Tensor:
        """Tensor from which to read the group size"""

    @tensor.setter
    def tensor(self, arg: Tensor, /) -> None: ...

    @property
    def offset(self) -> int:
        """Offset into the Tensor in bytes on where to start reading"""

    @offset.setter
    def offset(self, arg: int, /) -> None: ...

class Program(Resource):
    """
    Encapsulates a shader program enabling introspection into its bindings as well as keeping track of the parameters currently bound to them. Execution happens trough commands.
    """

    @overload
    def __init__(self, code: bytes) -> None:
        """
        Creates a new program using the shader's byte code

        Parameters
        ----------
        code: bytes
            Byte code of the program
        """

    @overload
    def __init__(self, code: bytes, specialization: bytes) -> None:
        """
        Creates a new program using the shader's byte code

        Parameters
        ----------
        code: bytes
            Byte code of the program
        specialization: bytes
            Data used for filling in specialization constants
        """

    @property
    def localSize(self) -> LocalSize:
        """Returns the size of the local work group."""

    @property
    def bindings(self) -> list[BindingTraits]:
        """Returns a list of all bindings."""

    @overload
    def isBindingBound(self, i: int) -> bool:
        """Checks wether the i-th binding is bound"""

    @overload
    def isBindingBound(self, name: str) -> bool:
        """Checks wether the binding specified by its name is bound"""

    def dispatch(self, x: int = 1, y: int = 1, z: int = 1) -> DispatchCommand:
        """
        Dispatches a program execution with the given amount of workgroups.

        Parameters
        ----------
        x: int, default=1
            Number of groups to dispatch in X dimension
        y: int, default=1
            Number of groups to dispatch in Y dimension
        z: int, default=1
            Number of groups to dispatch in Z dimension
        """

    def dispatchPush(self, push: bytes, x: int = 1, y: int = 1, z: int = 1) -> DispatchCommand:
        """
        Dispatches a program execution with the given push data and amount of workgroups.

        Parameters
        ----------
        push: bytes
           Data pushed to the dispatch as bytes
        x: int, default=1
            Number of groups to dispatch in X dimension
        y: int, default=1
            Number of groups to dispatch in Y dimension
        z: int, default=1
            Number of groups to dispatch in Z dimension
        """

    def dispatchIndirect(self, tensor: Tensor, offset: int = 0) -> DispatchIndirectCommand:
        """
        Dispatches a program execution using the amount of workgroups stored in the given tensor at the given offset. Expects the workgroup size as three consecutive unsigned 32 bit integers.

        Parameters
        ----------
        tensor: Tensor
            Tensor from which to read the amount of workgroups
        offset: int, default=0
            Offset at which to start reading
        """

    def dispatchIndirectPush(self, push: bytes, tensor: Tensor, offset: int = 0) -> DispatchIndirectCommand:
        """
        Dispatches a program execution with the given push data using the amount of workgroups stored in the given tensor at the given offset.

        Parameters
        ----------
        push: bytes
           Data pushed to the dispatch as bytes
        tensor: Tensor
            Tensor from which to read the amount of workgroups
        offset: int, default=0
            Offset at which to start reading
        """

    def __repr__(self) -> str: ...

class FlushMemoryCommand(Command):
    """Command for flushing memory writes"""

    def __init__(self) -> None: ...

def flushMemory() -> FlushMemoryCommand:
    """Returns a command for flushing memory writes."""

class DType(enum.Enum):
    int8 = 8

    int16 = 16

    int32 = 32

    int64 = 64

    uint8 = 264

    uint16 = 272

    uint32 = 288

    uint64 = 320

    float16 = 528

    float32 = 544

    float64 = 576

int8: DType = DType.int8

int16: DType = DType.int16

int32: DType = DType.int32

int64: DType = DType.int64

uint8: DType = DType.uint8

uint16: DType = DType.uint16

uint32: DType = DType.uint32

uint64: DType = DType.uint64

float16: DType = DType.float16

float32: DType = DType.float32

float64: DType = DType.float64

class Buffer(Resource):
    """
    Buffer for allocating a raw chunk of memory on the host accessible via its memory address. Useful as a base class providing more complex functionality.

    Parameters
    ----------
    size: int
        size of the buffer in bytes
    """

    def __init__(self, size: int) -> None: ...

    @property
    def address(self) -> int:
        """The memory address of the allocated buffer."""

    @property
    def nbytes(self) -> int:
        """The size of the buffer in bytes."""

    def __repr__(self) -> str: ...

class NDBuffer(Buffer):
    """
    Buffer allocating memory on the host accessible on the Python sidevia a numpy array.

    Parameters
    ----------
    shape
        Shape of the corresponding numpy array
    dtype: hephaistos::DType, default=float32
        Data type of the corresponding numpy array.
    """

    @overload
    def __init__(self, shape: int, *, dtype: DType = DType.float32) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, dtype: DType = DType.float32) -> None: ...

    def numpy(self) -> Annotated[ArrayLike, dict(device='cpu')]:
        """Returns numpy array using the buffer's memory"""

    @property
    def dtype(self) -> DType:
        """Underlying data type."""

    @property
    def ndim(self) -> int:
        """Number of dimensions of the underlying array"""

    @property
    def shape(self) -> tuple:
        """Shape of the underlying array"""

    @property
    def size(self) -> int:
        """Returns total number of items in the buffer or array."""

    def __repr__(self) -> str: ...

class Tensor(Resource):
    """Tensor allocating memory on the device."""

    @overload
    def __init__(self, size: int, *, mapped: bool = False) -> None:
        """
        Creates a new tensor of given size.

        Parameters
        ----------
        size: int
            Size of the tensor in bytes
        mapped: bool, default=False
            If True, tries to map the tensor to host address space.
        """

    @overload
    def __init__(self, size: int, *, addr: int, mapped: bool = False) -> None:
        """
        Creates a new tensor and fills it with the provided data

        Parameters
        ----------
        addr: int
            Address of the data used to fill the tensor
        n: int
            Number of bytes to copy from addr
        mapped: bool, default=False
            If True, tries to map memory to host address space
        """

    @overload
    def __init__(self, array: Annotated[ArrayLike, dict(order='C', device='cpu', writable=False)], *, mapped: bool = False) -> None:
        """
        Creates a new tensor and fills it with the provided data

        Parameters
        ----------
        array: NDArray
            Numpy array containing the data used to fill the tensor. Its type must match the tensor's.
        mapped: bool, default=False
            If True, tries to map memory to host address space
        """

    @property
    def address(self) -> int:
        """The device address of this tensor."""

    @property
    def isMapped(self) -> bool:
        """True, if the underlying memory is writable by the CPU."""

    @property
    def memory(self) -> int:
        """
        Mapped memory address of the tensor as seen from the CPU. Zero if not mapped.
        """

    @property
    def nbytes(self) -> int:
        """The size of the tensor in bytes."""

    @property
    def isNonCoherent(self) -> bool:
        """
        Wether calls to flush() and invalidate() are necessary to make changesin mapped memory between devices and host available
        """

    def update(self, addr: int, n: int, offset: int = 0) -> None:
        """
        Updates the tensor at the given offset with n elements from addr

        Parameters
        ----------
        ptr: int
           Address of memory to copy from
        n: int
           Amount of elements to copy
        offset: int, default=0
           Offset into the tensor in number of elements where the copy starts
        """

    def flush(self, offset: int = 0, size: int | None = None) -> None:
        """
        Makes writes in mapped memory from the host available to the device

        Parameters
        ----------
        offset: int, default=0
           Offset in amount of elements into mapped memory to flush
        size: int | None, default=None
           Number of elements to flush starting at offset. If None, flushes all remaining elements
        """

    def retrieve(self, addr: int, n: int, offset: int = 0) -> None:
        """
        Retrieves data from the tensor at the given offset and stores it in dst. Only needed if isNonCoherent is True.

        Parameters
        ----------
        ptr: int
           Address of memory to copy to
        n: int
           Amount of elements to copy
        offset: int, default=0
           Offset into the tensor in amount of elements where the copy starts
        """

    def invalidate(self, offset: int = 0, size: int | None = None) -> None:
        """
        Makes writes in mapped memory from the device available to the host. Only needed if isNonCoherent is True.

        Parameters
        ----------
        offset: int, default=0
           Offset in amount of elements into mapped memory to invalidate
        size: int | None, default=None
           Number of elements to invalidate starting at offset. If None, invalidates all remaining bytes
        """

    @overload
    def bindParameter(self, program: Program, binding: int) -> None:
        """Binds the tensor to the program at the given binding"""

    @overload
    def bindParameter(self, program: Program, binding: str) -> None: ...

    def __repr__(self) -> str: ...

class CharBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class ShortBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class IntBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class LongBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class ByteBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class UnsignedShortBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class UnsignedIntBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class UnsignedLongBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class HalfBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class FloatBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class DoubleBuffer(NDBuffer):
    @overload
    def __init__(self, size: int) -> None: ...

    @overload
    def __init__(self, shape: tuple[int]) -> None: ...

class CharTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class ShortTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class IntTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class LongTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class ByteTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class UnsignedShortTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class UnsignedIntTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class UnsignedLongTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class HalfTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class FloatTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class DoubleTensor(Tensor):
    @overload
    def __init__(self, _size: int, *, mapped: bool = False) -> None: ...

    @overload
    def __init__(self, shape: tuple[int], *, mapped: bool = False) -> None: ...

class RetrieveTensorCommand(Command):
    """Command for copying the src tensor back to the destination buffer"""

    def __init__(self, src: Tensor, dst: Buffer, bufferOffset: int | None = None, tensorOffset: int | None = None, size: int | None = None, unsafe: bool = False) -> None: ...

def retrieveTensor(src: Tensor, dst: Buffer, bufferOffset: int | None = None, tensorOffset: int | None = None, size: int | None = None, unsafe: bool = False) -> RetrieveTensorCommand:
    """
    Creates a command for copying the src tensor back to the destination buffer

    Parameters
    ----------
    src: Tensor
        Source tensor
    dst: Buffer
        Destination buffer
    bufferOffset: None|int, default=None
        Optional offset into the buffer in bytes
    tensorOffset: None|int, default=None
        Optional offset into the tensor in bytes
    size: None|int, default=None
        Amount of data to copy in bytes. If None, equals to the complete buffer
    unsafe: bool, default=False
       Wether to omit barriers ensuring read after write ordering
    """

class UpdateTensorCommand(Command):
    """Command for copying the src buffer into the destination tensor"""

    def __init__(self, src: Buffer, dst: Tensor, bufferOffset: int | None = None, tensorOffset: int | None = None, size: int | None = None, unsafe: bool = False) -> None: ...

def updateTensor(src: Buffer, dst: Tensor, bufferOffset: int | None = None, tensorOffset: int | None = None, size: int | None = None, unsafe: bool = False) -> UpdateTensorCommand:
    """
    Creates a command for copying the src buffer into the destination tensor

    Parameters
    ----------
    src: Buffer
        Source Buffer
    dst: Tensor
        Destination Tensor
    bufferOffset: None|int, default=None
        Optional offset into the buffer in bytes
    tensorOffset: None|int, default=None
        Optional offset into the tensor in bytes
    size: None|int, default=None
        Amount of data to copy in bytes. If None, equals to the complete buffer
    unsafe: bool, default=False
       Wether to omit barriers ensuring read after write ordering
    """

class ClearTensorCommand(Command):
    """Command for filling a tensor with constant data over a given range"""

    def __init__(self, tensor: Tensor, offset: int | None = None, size: int | None = None, data: int | None = None, unsafe: bool = False) -> None:
        """
        Creates a command for filling a tensor with constant data over a given range. Defaults to zeroing the complete tensor
        """

def clearTensor(tensor: Tensor, offset: int | None = None, size: int | None = None, data: int | None = None, unsafe: bool = False) -> ClearTensorCommand:
    """
    Creates a command for filling a tensor with constant data over a given range. Defaults to zeroing the complete tensor

    Parameters
    ----------
    tensor: Tensor
        Tensor to be modified
    offset: None|int, default=None
        Offset into the Tensor at which to start clearing it. Defaults to the start of the Tensor.
    size: None|int, default=None
        Amount of bytes to clear. If None, equals to the range starting at offset until the end of the tensor
    data: None|int, default=None
        32 bit integer used to fill the tensor. If None, uses all zeros.
    unsafe: bool, default=false
       Wether to omit barriers ensuring read after write ordering.
    """

class ImageFormat(enum.Enum):
    """List of supported image formats"""

    R8G8B8A8_UNORM = 37

    R8G8B8A8_SNORM = 38

    R8G8B8A8_UINT = 41

    R8G8B8A8_SINT = 42

    R16G16B16A16_UINT = 95

    R16G16B16A16_SINT = 96

    R32_UINT = 98

    R32_SINT = 99

    R32_SFLOAT = 100

    R32G32_UINT = 101

    R32G32_SINT = 102

    R32G32_SFLOAT = 103

    R32G32B32A32_UINT = 107

    R32G32B32A32_SINT = 108

    R32G32B32A32_SFLOAT = 109

R8G8B8A8_UNORM: ImageFormat = ImageFormat.R8G8B8A8_UNORM

R8G8B8A8_SNORM: ImageFormat = ImageFormat.R8G8B8A8_SNORM

R8G8B8A8_UINT: ImageFormat = ImageFormat.R8G8B8A8_UINT

R8G8B8A8_SINT: ImageFormat = ImageFormat.R8G8B8A8_SINT

R16G16B16A16_UINT: ImageFormat = ImageFormat.R16G16B16A16_UINT

R16G16B16A16_SINT: ImageFormat = ImageFormat.R16G16B16A16_SINT

R32_UINT: ImageFormat = ImageFormat.R32_UINT

R32_SINT: ImageFormat = ImageFormat.R32_SINT

R32_SFLOAT: ImageFormat = ImageFormat.R32_SFLOAT

R32G32_UINT: ImageFormat = ImageFormat.R32G32_UINT

R32G32_SINT: ImageFormat = ImageFormat.R32G32_SINT

R32G32_SFLOAT: ImageFormat = ImageFormat.R32G32_SFLOAT

R32G32B32A32_UINT: ImageFormat = ImageFormat.R32G32B32A32_UINT

R32G32B32A32_SINT: ImageFormat = ImageFormat.R32G32B32A32_SINT

R32G32B32A32_SFLOAT: ImageFormat = ImageFormat.R32G32B32A32_SFLOAT

def getElementSize(format: ImageFormat) -> int:
    """Returns the size of a single channel in bytes"""

class Image(Resource):
    """
    Allocates memory on the device using a memory layout it deems optimal for images presenting it inside programs as storage images thus allowing reads and writes to it.

    Parameters
    ----------
    format: ImageFormat
        Format of the image
    width: int
        Width of the image in pixels
    height: int, default=1
        Height of the image in pixels
    depth: int, default=1
        Depth of the image in pixels
    """

    def __init__(self, format: ImageFormat, width: int, height: int = 1, depth: int = 1) -> None: ...

    @property
    def width(self) -> int:
        """With of the image in pixels"""

    @property
    def height(self) -> int:
        """Height of the image in pixels"""

    @property
    def depth(self) -> int:
        """Depth of the image in pixels"""

    @property
    def format(self) -> ImageFormat:
        """Format of the image"""

    @property
    def size_bytes(self) -> int:
        """
        Size the image takes in a linear/compact memory layout in bytes. This can differ from the actual size the image takes on the device but can be useful to allocate buffers for transferring the image.
        """

    @overload
    def bindParameter(self, program: Program, binding: int) -> None:
        """Binds the image to the program at the given binding"""

    @overload
    def bindParameter(self, program: Program, binding: str) -> None: ...

class Texture(Resource):
    """
    Allocates memory on the device using a memory layout it deems optimal for images and presents it inside programs as texture allowing filtered lookups. The filter methods can specified

    Parameters
    ----------
    format: ImageFormat
        Format of the image
    width: int
        Width of the image in pixels
    height: int, default=1
        Height of the image in pixels
    depth: int, default=1
        Depth of the image in pixels
    filter: 'nearest'|'n'|'linear'|'l', default='linear'
        Method used to interpolate between pixels
    unnormalized: bool, default=False
        If True, use coordinates in pixel space rather than normalized ones inside programs
    modeU: 'repeat'|'r'|'mirrored repeat'|'mr'|'clamp edge'|'ce'|'mirrored clamp edge'|'mce', default='repeat'
        Method used to handle out of range coordinates in U dimension
    modeV: 'repeat'|'r'|'mirrored repeat'|'mr'|'clamp edge'|'ce'|'mirrored clamp edge'|'mce', default='repeat'
        Method used to handle out of range coordinates in V dimension
    modeW: 'repeat'|'r'|'mirrored repeat'|'mr'|'clamp edge'|'ce'|'mirrored clamp edge'|'mce', default='repeat'
        Method used to handle out of range coordinates in W dimension
    """

    def __init__(self, format: ImageFormat, width: int, height: int = 1, depth: int = 1, **kwargs) -> None: ...

    @property
    def width(self) -> int:
        """Width of the texture in pixels"""

    @property
    def height(self) -> int:
        """Height of the texture in pixels"""

    @property
    def depth(self) -> int:
        """Depth of the texture in pixels"""

    @property
    def format(self) -> ImageFormat:
        """Format of the texture"""

    @property
    def size_bytes(self) -> int:
        """
        Size the texture takes in a linear/compact memory layout in bytes. This can differ from the actual size the texture takes on the device but can be useful to allocate buffers for transferring the texture.
        """

    @overload
    def bindParameter(self, program: Program, binding: int) -> None:
        """Binds the texture to the program at the given binding"""

    @overload
    def bindParameter(self, program: Program, binding: str) -> None: ...

class ImageBuffer(Buffer):
    """
    Utility class allocating memory on the host side in linear memory layout allowing easy manipulating of 2D 32bit RGBA image data that can later be copied to an image or texture. Provides additional methods for loading and saving image data from and to disk in various file formats.

    Parameters
    ----------
    width: int
        Width of the image in pixels
    height: int
        Height of the image in pixels
    """

    def __init__(self, width: int, height: int) -> None: ...

    @property
    def width(self) -> int:
        """Width of the image in pixels"""

    @property
    def height(self) -> int:
        """Height of the image in pixels"""

    def save(self, filename: str) -> None:
        """Saves the image under the given filepath"""

    @staticmethod
    def loadFile(filename: str) -> ImageBuffer:
        """Loads the image at the given filepath and returns a new ImageBuffer"""

    @staticmethod
    def loadMemory(data: bytes) -> ImageBuffer:
        """
        Loads serialized image data from memory and returns a new ImageBuffer

        Parameters
        ----------
        data: bytes
            Binary data containing the image data
        """

    def numpy(self) -> Annotated[ArrayLike, dict(dtype='uint8', shape=(None, None, 4))]:
        """
        Returns a numpy array that allows to manipulate the data handled by this ImageBuffer
        """

class RetrieveImageCommand(Command):
    """Command for copying the image back into the given buffer"""

    def __init__(self, src: Image, dst: Buffer) -> None: ...

def retrieveImage(src: Image, dst: Buffer) -> RetrieveImageCommand:
    """
    src: Image
        Source image
    dst: Buffer
        Destination buffer
    """

class UpdateImageCommand(Command):
    """Command for copying data from the given buffer into the image"""

    def __init__(self, src: Buffer, dst: Image) -> None: ...

def updateImage(src: Buffer, dst: Image) -> UpdateImageCommand:
    """
    src: Buffer
        Source buffer
    dst: Image
        Destination image
    """

class UpdateTextureCommand(Command):
    """Command for copying data from the given buffer into the texture"""

    def __init__(self, src: Buffer, dst: Texture) -> None: ...

def updateTexture(src: Buffer, dst: Texture) -> UpdateTextureCommand:
    """
    src: Buffer
        Source buffer
    dst: Texture
        Destination texture
    """

class StopWatch:
    """Allows the measuring of elapsed time between commands execution"""

    def __init__(self) -> None:
        """Creates a new stopwatch for measuring elapsed time between commands."""

    def start(self) -> Command:
        """Returns the command to start the stop watch."""

    def stop(self) -> Command:
        """
        Returns the command to stop the stop watch. Can be recorded multiple times to record up to stopCount stop times.
        """

    def reset(self) -> None:
        """Resets the stop watch."""

    def getElapsedTime(self, wait: bool = False) -> float:
        """
        Calculates the elapsed time between the timestamps the device recorded during its execution of the start() end stop() command in nanoseconds. If wait is true, blocks the call until both timestamps are recorded, otherwise returns NaN if they are not yet available.
        """

class MeshVector:
    """List of Mesh"""

    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: MeshVector) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[Mesh], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[Mesh]: ...

    @overload
    def __getitem__(self, arg: int, /) -> Mesh: ...

    @overload
    def __getitem__(self, arg: slice, /) -> MeshVector: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: Mesh, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: Mesh, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> Mesh:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: MeshVector, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: Mesh, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: MeshVector, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

class GeometryVector:
    """List of Geometry"""

    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: GeometryVector) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[Geometry], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[Geometry]: ...

    @overload
    def __getitem__(self, arg: int, /) -> Geometry: ...

    @overload
    def __getitem__(self, arg: slice, /) -> GeometryVector: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: Geometry, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: Geometry, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> Geometry:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: GeometryVector, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: Geometry, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: GeometryVector, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

class GeometryInstanceVector:
    """List of GeometryInstance"""

    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: GeometryInstanceVector) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[GeometryInstance], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[GeometryInstance]: ...

    @overload
    def __getitem__(self, arg: int, /) -> GeometryInstance: ...

    @overload
    def __getitem__(self, arg: slice, /) -> GeometryInstanceVector: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: GeometryInstance, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: GeometryInstance, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> GeometryInstance:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: GeometryInstanceVector, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: GeometryInstance, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: GeometryInstanceVector, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

def isRaytracingSupported(id: int | None = None) -> bool:
    """Checks wether any or the given device supports ray tracing."""

def isRaytracingEnabled() -> bool:
    """
    Checks wether ray tracing was enabled. Note that this creates the context.
    """

def enableRaytracing(force: bool = False) -> None:
    """
    Enables ray tracing. (Lazy) context creation fails if not supported. Set force=True if an existing context should be destroyed.
    """

class Mesh:
    """
    Representation of a geometric shape consisting of triangles defined by their vertices, which can optionally be indexed. Meshes are used to build Geometries.
    """

    def __init__(self) -> None: ...

    @property
    def vertices(self) -> Annotated[ArrayLike, dict(dtype='float32', shape=(None, None), order='C', device='cpu')]:
        """
        Numpy array holding the vertex data. The first three columns must be the x, y and z positions.
        """

    @vertices.setter
    def vertices(self, arg: Annotated[ArrayLike, dict(dtype='float32', shape=(None, None), order='C', device='cpu')], /) -> None: ...

    @property
    def indices(self) -> Annotated[ArrayLike, dict(dtype='uint32', shape=(None, 3), order='C', device='cpu')]:
        """
        Optional numpy array holding the indices referencing vertices to create triangles.
        """

    @indices.setter
    def indices(self, arg: Annotated[ArrayLike, dict(dtype='uint32', shape=(None, 3), order='C', device='cpu')], /) -> None: ...

class Geometry:
    """
    Underlying structure Acceleration Structures use to trace rays against constructed from Meshes.
    """

    def __init__(self) -> None: ...

    @property
    def blas_address(self) -> int:
        """device address of the underlying blas"""

    @blas_address.setter
    def blas_address(self, arg: int, /) -> None: ...

    @property
    def vertices_address(self) -> int:
        """device address of the vertex buffer or zero if it was discarded"""

    @vertices_address.setter
    def vertices_address(self, arg: int, /) -> None: ...

    @property
    def indices_address(self) -> int:
        """
        device address of the index buffer, or zero if it was discarded or is non existent
        """

    @indices_address.setter
    def indices_address(self, arg: int, /) -> None: ...

class GeometryInstance:
    """
    Building blocks of Acceleration Structures containing a reference to a Geometry along a transformation to be applied to the underlying mesh as well as additional information.
    """

    def __init__(self) -> None: ...

    @property
    def blas_address(self) -> int:
        """device address of the referenced BLAS/geometry"""

    @blas_address.setter
    def blas_address(self, arg: int, /) -> None: ...

    @property
    def transform(self) -> Annotated[ArrayLike, dict(dtype='float32', shape=(3, 4), order='C', device='cpu')]:
        """The transformation applied to the referenced geometry."""

    @transform.setter
    def transform(self, arg: Annotated[ArrayLike, dict(dtype='float32', shape=(3, 4), order='C', device='cpu')], /) -> None: ...

    @property
    def customIndex(self) -> int:
        """The custom index of this instance available in the shader."""

    @customIndex.setter
    def customIndex(self, arg: int, /) -> None: ...

    @property
    def mask(self) -> int:
        """Mask of this instance used for masking ray traces."""

    @mask.setter
    def mask(self, arg: int, /) -> None: ...

class GeometryStore(Resource):
    """If True, keeps the mesh data on the GPU after building Geometries."""

    def __init__(self, meshes: MeshVector, keepMeshData: bool = True) -> None:
        """
        Creates a geometry store responsible for managing the BLAS/geometries used to create and run acceleration structures.
        """

    @property
    def geometries(self) -> GeometryVector:
        """Returns the list of stored geometries"""

    @property
    def size(self) -> int:
        """Number of geometries stored"""

    def createInstance(self, idx: int) -> GeometryInstance:
        """Creates a new instance of the specified geometry"""

class AccelerationStructure(Resource):
    """
    Acceleration Structure used by programs to trace rays against a scene. Consists of multiple instances of various Geometries.

    Parameters
    ---------
    instances: GeometryInstance[]
        list of instances the structure consists of
    """

    def __init__(self, instances: GeometryInstanceVector) -> None:
        """
        Creates an acceleration structure for consumption in shaders from the given geometry instances.
        """

    @overload
    def bindParameter(self, program: Program, binding: int) -> None:
        """Binds the acceleration structure to the program at the given binding"""

    @overload
    def bindParameter(self, program: Program, binding: str) -> None: ...

class AtomicsProperties:
    """List of atomic functions a device supports or are enabled"""

    @property
    def bufferInt64Atomics(self) -> bool: ...

    @property
    def bufferFloat16Atomics(self) -> bool: ...

    @property
    def bufferFloat16AtomicAdd(self) -> bool: ...

    @property
    def bufferFloat16AtomicMinMax(self) -> bool: ...

    @property
    def bufferFloat32Atomics(self) -> bool: ...

    @property
    def bufferFloat32AtomicAdd(self) -> bool: ...

    @property
    def bufferFloat32AtomicMinMax(self) -> bool: ...

    @property
    def bufferFloat64Atomics(self) -> bool: ...

    @property
    def bufferFloat64AtomicAdd(self) -> bool: ...

    @property
    def bufferFloat64AtomicMinMax(self) -> bool: ...

    @property
    def sharedInt64Atomics(self) -> bool: ...

    @property
    def sharedFloat16Atomics(self) -> bool: ...

    @property
    def sharedFloat16AtomicAdd(self) -> bool: ...

    @property
    def sharedFloat16AtomicMinMax(self) -> bool: ...

    @property
    def sharedFloat32Atomics(self) -> bool: ...

    @property
    def sharedFloat32AtomicAdd(self) -> bool: ...

    @property
    def sharedFloat32AtomicMinMax(self) -> bool: ...

    @property
    def sharedFloat64Atomics(self) -> bool: ...

    @property
    def sharedFloat64AtomicAdd(self) -> bool: ...

    @property
    def sharedFloat64AtomicMinMax(self) -> bool: ...

    @property
    def imageInt64Atomics(self) -> bool: ...

    @property
    def imageFloat32Atomics(self) -> bool: ...

    @property
    def imageFloat32AtomicAdd(self) -> bool: ...

    @property
    def imageFloat32AtomicMinMax(self) -> bool: ...

    def __repr__(self) -> str: ...

def getAtomicsProperties(id: int) -> AtomicsProperties:
    """Returns the atomic capabilities of the device given by its id"""

def getEnabledAtomics() -> AtomicsProperties:
    """Returns the in the current context enabled atomic features"""

def enableAtomics(flags: set, force: bool = False) -> None:
    """
    Enables the atomic features contained in the given set by their name. Set force=True if an existing context should be destroyed.
    """

class TypeSupport:
    """List of optional type support in programs"""

    @property
    def float64(self) -> bool: ...

    @property
    def float16(self) -> bool: ...

    @property
    def int64(self) -> bool: ...

    @property
    def int16(self) -> bool: ...

    @property
    def int8(self) -> bool: ...

    def __repr__(self) -> str: ...

def getSupportedTypes(id: int | None = None) -> TypeSupport:
    """Queries the supported extended types"""

def requireTypes(types: set, force: bool = False) -> None:
    """
    Forces the given types, i.e. devices not supported will be considerednot suitable. Set force=True if an existing context should be destroyed
    """

class DebugMessageSeverityFlagBits(enum.Enum):
    """Flags indicating debug message severity"""

    VERBOSE = 1

    INFO = 16

    WARNING = 256

    ERROR = 4096

VERBOSE: DebugMessageSeverityFlagBits = DebugMessageSeverityFlagBits.VERBOSE

INFO: DebugMessageSeverityFlagBits = DebugMessageSeverityFlagBits.INFO

WARNING: DebugMessageSeverityFlagBits = DebugMessageSeverityFlagBits.WARNING

ERROR: DebugMessageSeverityFlagBits = DebugMessageSeverityFlagBits.ERROR

class DebugMessage:
    """Debug message"""

    @property
    def idName(self) -> str: ...

    @property
    def idNumber(self) -> int: ...

    @property
    def message(self) -> str: ...

    def __str__(self) -> str: ...

def isDebugAvailable() -> bool:
    """Checks whether debugging is available"""

def configureDebug(enablePrint: bool = False, enableGPUValidation: bool = False, enableSynchronizationValidation: bool = False, enableThreadSafetyValidation: bool = False, enableAPIValidation: bool = False, callback: Callable[[DebugMessage], None] | None = None) -> None:
    """Configures the debug state"""
