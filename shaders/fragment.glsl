#version 330 core

struct PointLight {
    vec3 position;
    vec3 color;
    float strength;
};

in vec2 fragmentTexCoord;
in vec3 fragmentPos;
in vec3 fragmentNormal;

uniform sampler2D imageTexture;
uniform PointLight Lights[8];
uniform vec3 cameraPos;

out vec4 color;

vec3 calculatePointLight(PointLight light, vec3 fragmentPos, vec3 fragmentNormal);

void main()
{
    vec4 baseTexture = texture(imageTexture, fragmentTexCoord);

     // ambient
    vec3 temp = 0.2 * baseTexture.rgb;

    for (int i = 0; i < 8; i++) {
        temp += calculatePointLight(Lights[i], fragmentPos, fragmentNormal);
    }
    color = vec4(temp, baseTexture.a);
}

vec3 calculatePointLight(PointLight light, vec3 fragmentPos, vec3 fragmentNormal){
    vec3 result = vec3(0.0);
    vec3 baseTexture = texture(imageTexture, fragmentTexCoord).rgb;

    vec3 fragLight = light.position - fragmentPos;
    float distance = length(fragLight);
    fragLight = normalize(fragLight);

    vec3 fragCamera = normalize(cameraPos - fragmentPos);
    vec3 halfVec = normalize(fragLight + fragCamera);

    // diffuse
    result += light.color * light.strength * max(0.0, dot(fragmentNormal, fragLight)) / (distance * distance) * baseTexture;

    // specular
    result += light.color * light.strength * pow(max(0.0, dot(fragmentNormal, halfVec)), 32) / (distance * distance);

    return result;
}