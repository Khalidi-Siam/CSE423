'''OpenGL extension KHR.debug

This module customises the behaviour of the 
OpenGL.raw.GLES1.KHR.debug to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows the GL to notify applications when various events 
	occur that may be useful during application development, debugging and 
	profiling.
	
	These events are represented in the form of enumerable messages with a 
	human-readable string representation. Examples of debug events include 
	incorrect use of the GL, warnings of undefined behavior, and performance 
	warnings.
	
	A message is uniquely identified by a source, a type and an 
	implementation-dependent ID within the source and type pair.
	
	A message's source identifies the origin of the message and can either 
	describe components of the GL, the window system, third-party external 
	sources such as external debuggers, or even the application itself.
	
	The type of the message roughly identifies the nature of the event that 
	caused the message. Examples include errors, performance warnings, 
	warnings about undefined behavior or notifications identifying that the 
	application is within a specific section of the application code.
	
	A message's ID for a given source and type further distinguishes messages 
	within namespaces. For example, an error caused by a negative parameter 
	value or an invalid internal texture format are both errors generated by 
	the API, but would likely have different message IDs.
	
	Each message is also assigned to a severity level that denotes roughly how 
	"important" that message is in comparison to other messages across all 
	sources and types. For example, notification of a GL error would likely 
	have a higher severity than a performance warning due to redundant state 
	changes.
	
	Furthermore, every message contains an implementation-dependent string
	representation that provides a useful description of the event.
	
	Messages are communicated to the application through an application-
	defined callback function that is called by the GL implementation on each 
	debug message. The motivation for the callback routine is to free 
	application developers from actively having to query whether a GL error, 
	or any other debuggable event has happened after each call to a GL 
	function. With a callback, developers can keep their code free of debug 
	checks, set breakpoints in the callback function, and only have to react 
	to messages as they occur. In situations where using a callback is not 
	possible, a message log is also provided that stores only copies of recent 
	messages until they are actively queried. 
	
	To control the volume of debug output, messages can be disabled either 
	individually by ID, or entire sets of messages can be turned off based on 
	combination of source and type, through the entire application code or 
	only section of the code encapsulated in debug groups. A debug group may 
	also be used to annotate the command stream using descriptive texts. 
	
	This extension also defines debug markers, a mechanism for the OpenGL 
	application to annotate the command stream with markers for discrete 
	events.
	
	When profiling or debugging an OpenGL application with a built-in or an 
	external debugger or profiler, it is difficult to relate the commands 
	within the command stream to the elements of the scene or parts of the 
	program code to which they correspond. Debug markers and debug groups help 
	obviate this by allowing applications to specify this link. For example, a 
	debug marker can be used to identify the beginning of a frame in the 
	command stream and a debug group can encapsulate a specific command stream 
	to identify a rendering pass. Debug groups also allow control of the debug 
	outputs volume per section of an application code providing an effective 
	way to handle the massive amount of debug outputs that drivers can 
	generate.
	
	Some existing implementations of ARB_debug_output only expose the
	ARB_debug_output extension string if the context was created with the
	debug flag {GLX|WGL}_CONTEXT_DEBUG_BIT_ARB as specified in 
	{GLX|WGL}_ARB_create_context. The behavior is not obvious when the
	functionality is brought into the OpenGL core specification because the
	extension string and function entry points must always exist.
	
	This extension modifies the existing ARB_debug_output extension to allow 
	implementations to always have an empty message log. The specific messages 
	written to the message log or callback routines are already implementation 
	defined, so this specification simply makes it explicit that it's fine for 
	there to be zero messages generated, even when a GL error occurs, which is 
	useful if the context is non-debug.
	
	Debug output can be enabled and disabled by changing the DEBUG_OUTPUT 
	state. It is implementation defined how much debug output is generated if 
	the context was created without the CONTEXT_DEBUG_BIT set. This is a new 
	query bit added to the existing GL_CONTEXT_FLAGS state to specify whether 
	the context was created with debug enabled.
	
	Finally, this extension defines a mechanism for OpenGL applications to 
	label their objects (textures, buffers, shaders, etc.) with a descriptive 
	string. 
	
	When profiling or debugging an OpenGL application within an external or 
	built-in (debut output API) debugger or profiler it is difficult to 
	identify objects from their object names (integers). 
	
	Even when the object itself is viewed it can be problematic to 
	differentiate between similar objects. Attaching a descriptive string, a 
	label, to an object obviates this difficulty.
	
	The intended purpose of this extension is purely to improve the user 
	experience within OpenGL development tools and application built-in 
	profilers and debuggers. This extension typically improves OpenGL 
	programmers efficiency by allowing them to instantly detect issues and the 
	reason for these issues giving him more time to focus on adding new 
	features to an OpenGL application.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/KHR/debug.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.KHR.debug import *
from OpenGL.raw.GLES1.KHR.debug import _EXTENSION_NAME

def glInitDebugKHR():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glDebugMessageControl.ids size not checked against count
glDebugMessageControl=wrapper.wrapper(glDebugMessageControl).setInputArraySize(
    'ids', None
)
# INPUT glDebugMessageInsert.buf size not checked against 'buf,length'
glDebugMessageInsert=wrapper.wrapper(glDebugMessageInsert).setInputArraySize(
    'buf', None
)
glGetDebugMessageLog=wrapper.wrapper(glGetDebugMessageLog).setOutput(
    'ids',size=lambda x:(x,),pnameArg='count',orPassIn=True
).setOutput(
    'lengths',size=lambda x:(x,),pnameArg='count',orPassIn=True
).setOutput(
    'messageLog',size=lambda x:(x,),pnameArg='bufSize',orPassIn=True
).setOutput(
    'severities',size=lambda x:(x,),pnameArg='count',orPassIn=True
).setOutput(
    'sources',size=lambda x:(x,),pnameArg='count',orPassIn=True
).setOutput(
    'types',size=lambda x:(x,),pnameArg='count',orPassIn=True
)
# INPUT glPushDebugGroup.message size not checked against 'message,length'
glPushDebugGroup=wrapper.wrapper(glPushDebugGroup).setInputArraySize(
    'message', None
)
# INPUT glObjectLabel.label size not checked against 'label,length'
glObjectLabel=wrapper.wrapper(glObjectLabel).setInputArraySize(
    'label', None
)
glGetObjectLabel=wrapper.wrapper(glGetObjectLabel).setOutput(
    'label',size=lambda x:(x,),pnameArg='bufSize',orPassIn=True
).setOutput(
    'length',size=(1,),orPassIn=True
)
# INPUT glObjectPtrLabel.label size not checked against 'label,length'
glObjectPtrLabel=wrapper.wrapper(glObjectPtrLabel).setInputArraySize(
    'label', None
)
glGetObjectPtrLabel=wrapper.wrapper(glGetObjectPtrLabel).setOutput(
    'label',size=lambda x:(x,),pnameArg='bufSize',orPassIn=True
).setOutput(
    'length',size=(1,),orPassIn=True
)
glGetPointerv=wrapper.wrapper(glGetPointerv).setOutput(
    'params',size=(1,),orPassIn=True
)
# INPUT glGetDebugMessageLogKHR.ids size not checked against count
# INPUT glGetDebugMessageLogKHR.lengths size not checked against count
# INPUT glGetDebugMessageLogKHR.messageLog size not checked against bufSize
# INPUT glGetDebugMessageLogKHR.severities size not checked against count
# INPUT glGetDebugMessageLogKHR.sources size not checked against count
# INPUT glGetDebugMessageLogKHR.types size not checked against count
glGetDebugMessageLogKHR=wrapper.wrapper(glGetDebugMessageLogKHR).setInputArraySize(
    'ids', None
).setInputArraySize(
    'lengths', None
).setInputArraySize(
    'messageLog', None
).setInputArraySize(
    'severities', None
).setInputArraySize(
    'sources', None
).setInputArraySize(
    'types', None
)
# INPUT glGetObjectLabelKHR.label size not checked against bufSize
glGetObjectLabelKHR=wrapper.wrapper(glGetObjectLabelKHR).setInputArraySize(
    'label', None
)
# INPUT glGetObjectPtrLabelKHR.label size not checked against bufSize
glGetObjectPtrLabelKHR=wrapper.wrapper(glGetObjectPtrLabelKHR).setInputArraySize(
    'label', None
).setInputArraySize(
    'length', 1
)
### END AUTOGENERATED SECTION