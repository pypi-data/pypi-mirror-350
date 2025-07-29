import wilson.run.smeft.beta as betamodule
import functools

# Global configuration for patching
key_var = None
new_value = None

def configure_patch(key, value):
    """
    Sets the key and value to patch the beta function with.
    """
    global key_var, new_value
    key_var = key
    new_value = value
    patch_wilson_beta(key)

def beta_editor(key, value):
    """
    Defines how the beta function value should be modified.
    """
    return new_value  # Can be made more complex if needed

def beta_wrapper(originalbeta, required_key):
    """
    Wraps the original beta function to intercept and modify specific keys.
    """
    @functools.wraps(originalbeta)
    def wrapped_beta(C, *args, **kwargs):
        # Extract 'scale' from args or kwargs
        scale = kwargs.get('scale', None)
        if scale is None:
            if len(args) >= 1:
                scale = args[0]
                args = args[1:]
            else:
                raise TypeError("patched beta() missing required argument: 'scale'")

        Beta = originalbeta(C, scale, *args, **kwargs)

        if required_key in Beta:
            Beta[required_key] = beta_editor(required_key, Beta[required_key])

        return Beta

    return wrapped_beta

def patch_wilson_beta(required_key):
    """
    Replaces the Wilson beta function with a wrapped version that modifies a specific key.
    """
    betamodule.beta = beta_wrapper(betamodule.beta, required_key)


